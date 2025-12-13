import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

class TestCompleteUserJourney:
    
    @pytest.fixture
    def driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()
    
    def test_new_user_complete_journey(self, driver):
        """Test complete journey: registration -> login -> booking -> payment -> checkin -> checkout"""
        
        # 1. User Registration
        driver.get("http://localhost:3000/signup")
        driver.find_element(By.ID, "name").send_keys("John Doe")
        driver.find_element(By.ID, "email").send_keys("john.doe@example.com")
        driver.find_element(By.ID, "password").send_keys("securepass123")
        driver.find_element(By.ID, "confirm_password").send_keys("securepass123")
        driver.find_element(By.ID, "signup-btn").click()
        
        WebDriverWait(driver, 10).until(EC.url_contains("/login"))
        
        # 2. User Login
        driver.find_element(By.ID, "email").send_keys("john.doe@example.com")
        driver.find_element(By.ID, "password").send_keys("securepass123")
        driver.find_element(By.ID, "login-btn").click()
        
        WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
        
        # 3. Browse and Select Space
        driver.get("http://localhost:3000/spaces")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "space-card"))
        )
        
        book_btn = driver.find_element(By.CLASS_NAME, "book-btn")
        book_btn.click()
        
        # 4. Make Reservation
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "booking-form"))
        )
        
        driver.find_element(By.ID, "booking-date").send_keys("2024-12-25")
        
        start_time = Select(driver.find_element(By.ID, "start-time"))
        start_time.select_by_value("14:00")
        
        end_time = Select(driver.find_element(By.ID, "end-time"))
        end_time.select_by_value("16:00")
        
        driver.find_element(By.ID, "confirm-booking-btn").click()
        
        # 5. Payment Process
        WebDriverWait(driver, 10).until(EC.url_contains("/payment"))
        
        driver.find_element(By.ID, "payment-card").click()
        driver.find_element(By.ID, "card-number").send_keys("4111111111111111")
        driver.find_element(By.ID, "card-name").send_keys("John Doe")
        driver.find_element(By.ID, "card-expiry").send_keys("12/25")
        driver.find_element(By.ID, "card-cvv").send_keys("123")
        
        driver.find_element(By.ID, "pay-btn").click()
        
        WebDriverWait(driver, 15).until(EC.url_contains("/payment/success"))
        
        # 6. Check-in Process
        driver.get("http://localhost:3000/reservations")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "reservation-card"))
        )
        
        checkin_btn = driver.find_element(By.CLASS_NAME, "checkin-btn")
        checkin_btn.click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "access-code"))
        )
        driver.find_element(By.ID, "access-code").send_keys("ABC123")
        driver.find_element(By.ID, "checkin-confirm-btn").click()
        
        success_msg = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "checkin-success"))
        )
        assert "checked in successfully" in success_msg.text.lower()
        
        # 7. Check-out Process
        checkout_btn = driver.find_element(By.CLASS_NAME, "checkout-btn")
        checkout_btn.click()
        
        driver.find_element(By.ID, "checkout-confirm-btn").click()
        
        checkout_msg = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "checkout-success"))
        )
        assert "checked out successfully" in checkout_msg.text.lower()