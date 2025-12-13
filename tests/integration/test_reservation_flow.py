import pytest
import requests
import json
import time
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

class TestReservationFlow:
    
    def setup_method(self):
        """Setup test data"""
        self.user_data = {
            'email': 'test@example.com',
            'password': 'test123',
            'name': 'Test User',
            'role': 'user'
        }
        self.space_data = {
            'name': 'Test Space',
            'description': 'Test Description',
            'capacity': 10,
            'price_per_hour': 25.0
        }
    
    def test_complete_reservation_flow(self):
        """Test complete flow: signup -> login -> create space -> reserve -> pay -> checkin"""
        
        # 1. User signup
        signup_response = requests.post(f"{BASE_URL}/auth/signup", json=self.user_data)
        assert signup_response.status_code == 201
        
        # 2. User login
        login_response = requests.post(f"{BASE_URL}/auth/login", 
            json={'email': self.user_data['email'], 'password': self.user_data['password']})
        assert login_response.status_code == 200
        token = login_response.json()['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # 3. Create space (admin action)
        space_response = requests.post(f"{BASE_URL}/spaces", json=self.space_data)
        assert space_response.status_code == 201
        space_id = space_response.json()['id']
        
        # 4. Calculate pricing
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        pricing_response = requests.post(f"{BASE_URL}/pricing/calc", json={
            'space_id': space_id,
            'hours': 2,
            'user_type': 'regular'
        })
        assert pricing_response.status_code == 200
        total_price = pricing_response.json()['total_price']
        
        # 5. Create reservation
        reservation_response = requests.post(f"{BASE_URL}/reservations", 
            json={
                'user_id': login_response.json()['user_id'],
                'space_id': space_id,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat()
            }, headers=headers)
        assert reservation_response.status_code == 201
        reservation_id = reservation_response.json()['id']
        
        # 6. Process payment
        payment_response = requests.post(f"{BASE_URL}/payments/charge", json={
            'reservation_id': reservation_id,
            'amount': total_price,
            'method': 'card',
            'user_id': login_response.json()['user_id'],
            'card_token': 'test_card_token'
        })
        assert payment_response.status_code == 200
        assert payment_response.json()['status'] == 'approved'
        
        # 7. Check-in
        checkin_response = requests.post(f"{BASE_URL}/checkin/{reservation_id}", json={
            'user_id': login_response.json()['user_id'],
            'access_code': 'ABC123'
        })
        assert checkin_response.status_code == 200
        assert checkin_response.json()['status'] == 'checked_in'
        
        # 8. Check-out
        checkout_response = requests.post(f"{BASE_URL}/checkout/{reservation_id}", json={
            'user_id': login_response.json()['user_id']
        })
        assert checkout_response.status_code == 200
        assert checkout_response.json()['status'] == 'checked_out'
    
    def test_reservation_cancellation_flow(self):
        """Test reservation cancellation and refund"""
        
        # Setup user and space
        requests.post(f"{BASE_URL}/auth/signup", json=self.user_data)
        login_response = requests.post(f"{BASE_URL}/auth/login", 
            json={'email': self.user_data['email'], 'password': self.user_data['password']})
        token = login_response.json()['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        space_response = requests.post(f"{BASE_URL}/spaces", json=self.space_data)
        space_id = space_response.json()['id']
        
        # Create and pay for reservation
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        reservation_response = requests.post(f"{BASE_URL}/reservations", 
            json={
                'user_id': login_response.json()['user_id'],
                'space_id': space_id,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat()
            }, headers=headers)
        reservation_id = reservation_response.json()['id']
        
        payment_response = requests.post(f"{BASE_URL}/payments/charge", json={
            'reservation_id': reservation_id,
            'amount': 50.0,
            'method': 'card',
            'user_id': login_response.json()['user_id'],
            'card_token': 'test_card_token'
        })
        payment_id = payment_response.json()['payment_id']
        
        # Cancel reservation
        cancel_response = requests.delete(f"{BASE_URL}/reservations/{reservation_id}")
        assert cancel_response.status_code == 200
        
        # Process refund
        refund_response = requests.post(f"{BASE_URL}/payments/refund", json={
            'payment_id': payment_id,
            'amount': 50.0
        })
        assert refund_response.status_code == 200
        assert refund_response.json()['status'] == 'refunded'