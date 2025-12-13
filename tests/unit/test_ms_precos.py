import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ms-precos'))

from app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_calculate_price_basic(client):
    response = client.post('/pricing/calc', json={
        'space_id': 'space123',
        'hours': 2,
        'user_type': 'regular'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'total_price' in data
    assert data['total_price'] > 0

def test_calculate_price_with_discount(client):
    response = client.post('/pricing/calc', json={
        'space_id': 'space123',
        'hours': 8,
        'user_type': 'premium'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'total_price' in data
    assert 'discount_applied' in data

def test_calculate_price_bulk_hours(client):
    response = client.post('/pricing/calc', json={
        'space_id': 'space123',
        'hours': 10,
        'user_type': 'regular'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['discount_applied'] > 0

def test_invalid_hours(client):
    response = client.post('/pricing/calc', json={
        'space_id': 'space123',
        'hours': 0,
        'user_type': 'regular'
    })
    assert response.status_code == 400

def test_weekend_pricing(client):
    response = client.post('/pricing/calc', json={
        'space_id': 'space123',
        'hours': 4,
        'user_type': 'regular',
        'is_weekend': True
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['weekend_surcharge'] > 0