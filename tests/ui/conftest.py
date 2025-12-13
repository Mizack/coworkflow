import pytest
import subprocess
import time
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def setup_ui_test_environment():
    """Setup environment for UI tests"""
    
    # Start Docker containers
    print("Starting services for UI tests...")
    subprocess.run(["docker-compose", "up", "-d"], 
                  cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    
    # Wait for frontend to be ready
    max_retries = 30
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:3000", timeout=5)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            pass
        
        if i == max_retries - 1:
            pytest.fail("Frontend failed to start within timeout")
        
        time.sleep(2)
    
    yield
    
    # Cleanup
    print("Stopping services...")
    subprocess.run(["docker-compose", "down"], 
                  cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

@pytest.fixture
def chrome_driver():
    """Create Chrome WebDriver instance"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()

@pytest.fixture
def clean_test_data():
    """Clean test data before each UI test"""
    # Reset database state
    try:
        requests.post("http://localhost:8000/test/reset-all")
    except requests.exceptions.RequestException:
        pass  # Service might not have reset endpoint
    
    yield

@pytest.fixture
def test_user_data():
    """Provide test user data"""
    return {
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    }

@pytest.fixture
def test_space_data():
    """Provide test space data"""
    return {
        'name': 'Test Meeting Room',
        'description': 'A comfortable meeting room for small teams',
        'capacity': 8,
        'price_per_hour': 25.0
    }