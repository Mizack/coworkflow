import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ms-espacos'))

from app import app, spaces_db
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            spaces_db.clear()
            yield client

def test_create_space(client):
    response = client.post('/spaces', 
        json={'name': 'Test Space', 'description': 'Test Desc', 'capacity': 10, 'price_per_hour': 25.0})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data

def test_get_spaces_empty(client):
    response = client.get('/spaces')
    assert response.status_code == 200
    assert json.loads(response.data) == []

def test_get_spaces_with_data(client):
    client.post('/spaces', 
        json={'name': 'Test Space', 'description': 'Test Desc', 'capacity': 10, 'price_per_hour': 25.0})
    response = client.get('/spaces')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['name'] == 'Test Space'

def test_get_space_by_id(client):
    create_response = client.post('/spaces', 
        json={'name': 'Test Space', 'description': 'Test Desc', 'capacity': 10, 'price_per_hour': 25.0})
    space_id = json.loads(create_response.data)['id']
    
    response = client.get(f'/spaces/{space_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Test Space'

def test_update_space(client):
    create_response = client.post('/spaces', 
        json={'name': 'Test Space', 'description': 'Test Desc', 'capacity': 10, 'price_per_hour': 25.0})
    space_id = json.loads(create_response.data)['id']
    
    response = client.put(f'/spaces/{space_id}', 
        json={'name': 'Updated Space', 'capacity': 15})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Updated Space'
    assert data['capacity'] == 15

def test_delete_space(client):
    create_response = client.post('/spaces', 
        json={'name': 'Test Space', 'description': 'Test Desc', 'capacity': 10, 'price_per_hour': 25.0})
    space_id = json.loads(create_response.data)['id']
    
    response = client.delete(f'/spaces/{space_id}')
    assert response.status_code == 200
    
    get_response = client.get(f'/spaces/{space_id}')
    assert get_response.status_code == 404