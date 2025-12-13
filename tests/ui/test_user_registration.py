import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

class TestUserRegistration:
    
    @pytest.fixture
    def driver(self):
        """Setup Chrome driver for tests"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()
    
    def test_successful_registration(self, driver):
        """Test successful user registration"""
        
        # Navigate to signup page
        driver.get("http://localhost:3000/signup")
        
        # Fill registration form
        driver.find_element(By.ID, "name").send_keys("Test User")
        driver.find_element(By.ID, "email").send_keys("test@example.com")
        driver.find_element(By.ID, "password").send_keys("password123")
        driver.find_element(By.ID, "confirm_password").send_keys("password123")
        
        # Submit form
        driver.find_element(By.ID, "signup-btn").click()
        
        # Wait for redirect to login page
        WebDriverWait(driver, 10).until(
            EC.url_contains("/login")
        )
        
        # Check for success message
        success_message = driver.find_element(By.CLASS_NAME, "alert-success")
        assert "Registration successful" in success_message.text
    
    def test_registration_with_existing_email(self, driver):
        """Test registration with already existing email"""
        
        driver.get("http://localhost:3000/signup")
        
        # Fill form with existing email
        driver.find_element(By.ID, "name").send_keys("Another User")
        driver.find_element(By.ID, "email").send_keys("existing@example.com")
        driver.find_element(By.ID, "password").send_keys("password123")
        driver.find_element(By.ID, "confirm_password").send_keys("password123")
        
        driver.find_element(By.ID, "signup-btn").click()
        
        # Check for error message
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
        )
        assert "Email already exists" in error_message.text
    
    def test_password_mismatch(self, driver):
        """Test registration with password mismatch"""
        
        driver.get("http://localhost:3000/signup")
        
        driver.find_element(By.ID, "name").send_keys("Test User")
        driver.find_element(By.ID, "email").send_keys("test2@example.com")
        driver.find_element(By.ID, "password").send_keys("password123")
        driver.find_element(By.ID, "confirm_password").send_keys("different123")
        
        driver.find_element(By.ID, "signup-btn").click()
        
        # Check for validation error
        error_message = driver.find_element(By.CLASS_NAME, "invalid-feedback")
        assert "Passwords do not match" in error_message.text
    
    def test_form_validation(self, driver):
        """Test form validation for required fields"""
        
        driver.get("http://localhost:3000/signup")
        
        # Try to submit empty form
        driver.find_element(By.ID, "signup-btn").click()
        
        # Check that required field validation appears
        name_field = driver.find_element(By.ID, "name")
        assert name_field.get_attribute("required") is not None
        
        email_field = driver.find_element(By.ID, "email")
        assert email_field.get_attribute("required") is not None