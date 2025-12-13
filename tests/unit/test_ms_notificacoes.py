import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ms-notificacoes'))

from app import app, notifications_db
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            notifications_db.clear()
            yield client

def test_send_email_success(client):
    response = client.post('/notify/email', json={
        'to': 'test@example.com',
        'subject': 'Test Subject',
        'body': 'Test message',
        'template': 'reservation_confirmation'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'sent'
    assert 'message_id' in data

def test_send_sms_success(client):
    response = client.post('/notify/sms', json={
        'to': '+5511999999999',
        'message': 'Your reservation is confirmed'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'sent'

def test_send_push_success(client):
    response = client.post('/notify/push', json={
        'user_id': 'user123',
        'title': 'Reservation Reminder',
        'body': 'Your reservation starts in 30 minutes'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'sent'

def test_invalid_email(client):
    response = client.post('/notify/email', json={
        'to': 'invalid-email',
        'subject': 'Test',
        'body': 'Test'
    })
    assert response.status_code == 400

def test_invalid_phone(client):
    response = client.post('/notify/sms', json={
        'to': 'invalid-phone',
        'message': 'Test'
    })
    assert response.status_code == 400

def test_get_notification_history(client):
    client.post('/notify/email', json={
        'to': 'test@example.com',
        'subject': 'Test',
        'body': 'Test'
    })
    
    response = client.get('/notify/history/user123')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)