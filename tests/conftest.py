import pytest
import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

@pytest.fixture(scope="session")
def test_config():
    """Test configuration"""
    return {
        'base_url': 'http://localhost:8000',
        'frontend_url': 'http://localhost:3000',
        'test_user': {
            'email': 'test@example.com',
            'password': 'test123',
            'name': 'Test User'
        },
        'admin_user': {
            'email': 'admin@coworkflow.com',
            'password': 'admin123'
        }
    }

@pytest.fixture
def api_headers():
    """Common API headers"""
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }