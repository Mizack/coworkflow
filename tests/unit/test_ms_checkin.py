import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ms-checkin'))

from app import app, checkins_db
import json
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            checkins_db.clear()
            yield client

def test_checkin_success(client):
    response = client.post('/checkin/res123', json={
        'user_id': 'user123',
        'access_code': 'ABC123'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'checked_in'
    assert 'checkin_time' in data

def test_checkout_success(client):
    # First checkin
    client.post('/checkin/res123', json={
        'user_id': 'user123',
        'access_code': 'ABC123'
    })
    
    response = client.post('/checkout/res123', json={
        'user_id': 'user123'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'checked_out'
    assert 'checkout_time' in data

def test_checkin_invalid_code(client):
    response = client.post('/checkin/res123', json={
        'user_id': 'user123',
        'access_code': 'WRONG'
    })
    assert response.status_code == 401

def test_checkout_without_checkin(client):
    response = client.post('/checkout/res123', json={
        'user_id': 'user123'
    })
    assert response.status_code == 400

def test_double_checkin(client):
    client.post('/checkin/res123', json={
        'user_id': 'user123',
        'access_code': 'ABC123'
    })
    
    response = client.post('/checkin/res123', json={
        'user_id': 'user123',
        'access_code': 'ABC123'
    })
    assert response.status_code == 400

def test_get_checkin_status(client):
    client.post('/checkin/res123', json={
        'user_id': 'user123',
        'access_code': 'ABC123'
    })
    
    response = client.get('/checkin/res123/status')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'checked_in'