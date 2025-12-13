import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ms-pagamentos'))

from app import app, payments_db
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            payments_db.clear()
            yield client

def test_charge_pix_success(client):
    response = client.post('/payments/charge', json={
        'reservation_id': 'res123',
        'amount': 50.0,
        'method': 'pix',
        'user_id': 'user123'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'pending'
    assert 'pix_code' in data

def test_charge_card_success(client):
    response = client.post('/payments/charge', json={
        'reservation_id': 'res123',
        'amount': 50.0,
        'method': 'card',
        'user_id': 'user123',
        'card_token': 'card_token_123'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'approved'

def test_charge_invalid_amount(client):
    response = client.post('/payments/charge', json={
        'reservation_id': 'res123',
        'amount': -10.0,
        'method': 'pix',
        'user_id': 'user123'
    })
    assert response.status_code == 400

def test_refund_success(client):
    # First create a payment
    charge_response = client.post('/payments/charge', json={
        'reservation_id': 'res123',
        'amount': 50.0,
        'method': 'card',
        'user_id': 'user123',
        'card_token': 'card_token_123'
    })
    payment_id = json.loads(charge_response.data)['payment_id']
    
    response = client.post('/payments/refund', json={
        'payment_id': payment_id,
        'amount': 50.0
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'refunded'

def test_refund_invalid_payment(client):
    response = client.post('/payments/refund', json={
        'payment_id': 'invalid_id',
        'amount': 50.0
    })
    assert response.status_code == 404