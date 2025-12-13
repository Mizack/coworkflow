import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ms-reservas'))

from app import app, reservations_db
import json
from datetime import datetime, timedelta

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            reservations_db.clear()
            yield client

def test_create_reservation(client):
    start_time = datetime.now() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)
    
    response = client.post('/reservations', json={
        'user_id': 'user123',
        'space_id': 'space456',
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat()
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert data['status'] == 'confirmed'

def test_get_reservations_by_user(client):
    start_time = datetime.now() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)
    
    client.post('/reservations', json={
        'user_id': 'user123',
        'space_id': 'space456',
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat()
    })
    
    response = client.get('/reservations/user/user123')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1

def test_cancel_reservation(client):
    start_time = datetime.now() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)
    
    create_response = client.post('/reservations', json={
        'user_id': 'user123',
        'space_id': 'space456',
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat()
    })
    reservation_id = json.loads(create_response.data)['id']
    
    response = client.delete(f'/reservations/{reservation_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'cancelled'

def test_invalid_time_range(client):
    start_time = datetime.now() + timedelta(hours=2)
    end_time = start_time - timedelta(hours=1)  # End before start
    
    response = client.post('/reservations', json={
        'user_id': 'user123',
        'space_id': 'space456',
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat()
    })
    assert response.status_code == 400