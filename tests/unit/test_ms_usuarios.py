import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ms-usuarios'))

from app import app, users_db
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            users_db.clear()
            yield client

def test_signup_success(client):
    response = client.post('/auth/signup', 
        json={'email': 'test@test.com', 'password': 'test123', 'name': 'Test User', 'role': 'user'})
    assert response.status_code == 201
    assert b'User created' in response.data

def test_signup_duplicate_email(client):
    client.post('/auth/signup', 
        json={'email': 'test@test.com', 'password': 'test123', 'name': 'Test User', 'role': 'user'})
    response = client.post('/auth/signup', 
        json={'email': 'test@test.com', 'password': 'test123', 'name': 'Test User2', 'role': 'user'})
    assert response.status_code == 400

def test_login_success(client):
    client.post('/auth/signup', 
        json={'email': 'test@test.com', 'password': 'test123', 'name': 'Test User', 'role': 'user'})
    response = client.post('/auth/login', 
        json={'email': 'test@test.com', 'password': 'test123'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data
    assert data['role'] == 'user'

def test_login_invalid_credentials(client):
    response = client.post('/auth/login', 
        json={'email': 'test@test.com', 'password': 'wrong'})
    assert response.status_code == 401

def test_get_user_me(client):
    client.post('/auth/signup', 
        json={'email': 'test@test.com', 'password': 'test123', 'name': 'Test User', 'role': 'user'})
    login_response = client.post('/auth/login', 
        json={'email': 'test@test.com', 'password': 'test123'})
    token = json.loads(login_response.data)['token']
    
    response = client.get('/users/me', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['email'] == 'test@test.com'
    assert data['name'] == 'Test User'