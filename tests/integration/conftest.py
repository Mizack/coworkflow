import pytest
import subprocess
import time
import requests
import os

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment by starting Docker containers"""
    
    # Start Docker containers
    print("Starting Docker containers for integration tests...")
    subprocess.run(["docker-compose", "up", "-d"], 
                  cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    
    # Wait for services to be ready
    max_retries = 30
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            pass
        
        if i == max_retries - 1:
            pytest.fail("Services failed to start within timeout")
        
        time.sleep(2)
    
    yield
    
    # Cleanup
    print("Stopping Docker containers...")
    subprocess.run(["docker-compose", "down"], 
                  cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

@pytest.fixture
def clean_database():
    """Clean database before each test"""
    # Reset all microservice databases
    services = ['users', 'spaces', 'reservations', 'payments', 'checkin', 'notifications']
    
    for service in services:
        try:
            requests.post(f"http://localhost:8000/{service}/test/reset")
        except requests.exceptions.RequestException:
            pass  # Service might not have reset endpoint
    
    yield