import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ms-financeiro'))

from app import app
import json
from datetime import datetime, timedelta

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_revenue_report(client):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    response = client.get('/financial/revenue', query_string={
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat()
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'total_revenue' in data
    assert 'period' in data

def test_get_expenses_report(client):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    response = client.get('/financial/expenses', query_string={
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat()
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'total_expenses' in data
    assert 'categories' in data

def test_get_profit_loss(client):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    response = client.get('/financial/profit-loss', query_string={
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat()
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'net_profit' in data
    assert 'gross_revenue' in data
    assert 'total_expenses' in data

def test_get_cash_flow(client):
    response = client.get('/financial/cash-flow')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'current_balance' in data
    assert 'projected_balance' in data

def test_invalid_date_range(client):
    end_date = datetime.now() - timedelta(days=30)
    start_date = datetime.now()
    
    response = client.get('/financial/revenue', query_string={
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat()
    })
    assert response.status_code == 400