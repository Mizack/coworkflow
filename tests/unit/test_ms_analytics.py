import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ms-analytics'))

from app import app
import json
from datetime import datetime, timedelta

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_usage_stats(client):
    response = client.get('/analytics/usage')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'total_reservations' in data
    assert 'occupancy_rate' in data
    assert 'popular_spaces' in data

def test_get_user_behavior(client):
    response = client.get('/analytics/users')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'active_users' in data
    assert 'new_users' in data
    assert 'retention_rate' in data

def test_get_revenue_analytics(client):
    response = client.get('/analytics/revenue')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'monthly_revenue' in data
    assert 'revenue_by_space' in data
    assert 'growth_rate' in data

def test_get_space_performance(client):
    response = client.get('/analytics/spaces/performance')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'spaces' in data
    assert isinstance(data['spaces'], list)

def test_get_dashboard_data(client):
    response = client.get('/analytics/dashboard')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'kpis' in data
    assert 'charts' in data
    assert 'alerts' in data

def test_get_custom_report(client):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    response = client.post('/analytics/custom-report', json={
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'metrics': ['revenue', 'occupancy', 'users'],
        'group_by': 'day'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'report_data' in data
    assert 'summary' in data