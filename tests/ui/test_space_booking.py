import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

class TestSpaceBooking:
    
    @pytest.fixture
    def driver(self):
        """Setup Chrome driver for tests"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()
    
    @pytest.fixture
    def logged_in_user(self, driver):
        """Login user before tests"""
        driver.get("http://localhost:3000/login")
        driver.find_element(By.ID, "email").send_keys("test@example.com")
        driver.find_element(By.ID, "password").send_keys("password123")
        driver.find_element(By.ID, "login-btn").click()
        
        WebDriverWait(driver, 10).until(
            EC.url_contains("/dashboard")
        )
        return driver
    
    def test_view_available_spaces(self, logged_in_user):
        """Test viewing available spaces"""
        
        # Navigate to spaces page
        logged_in_user.get("http://localhost:3000/spaces")
        
        # Wait for spaces to load
        WebDriverWait(logged_in_user, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "space-card"))
        )
        
        # Check that spaces are displayed
        space_cards = logged_in_user.find_elements(By.CLASS_NAME, "space-card")
        assert len(space_cards) > 0
        
        # Check space details are visible
        first_space = space_cards[0]
        assert first_space.find_element(By.CLASS_NAME, "space-name").text
        assert first_space.find_element(By.CLASS_NAME, "space-capacity").text
        assert first_space.find_element(By.CLASS_NAME, "space-price").text
    
    def test_successful_booking(self, logged_in_user):
        """Test successful space booking"""
        
        logged_in_user.get("http://localhost:3000/spaces")
        
        # Click on first available space
        first_space = WebDriverWait(logged_in_user, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "book-btn"))
        )
        first_space.click()
        
        # Fill booking form
        WebDriverWait(logged_in_user, 10).until(
            EC.presence_of_element_located((By.ID, "booking-form"))
        )
        
        # Select date (tomorrow)
        date_input = logged_in_user.find_element(By.ID, "booking-date")
        date_input.clear()
        date_input.send_keys("2024-12-25")  # Use future date
        
        # Select time
        start_time = Select(logged_in_user.find_element(By.ID, "start-time"))
        start_time.select_by_value("09:00")
        
        end_time = Select(logged_in_user.find_element(By.ID, "end-time"))
        end_time.select_by_value("11:00")
        
        # Submit booking
        logged_in_user.find_element(By.ID, "confirm-booking-btn").click()
        
        # Wait for payment page
        WebDriverWait(logged_in_user, 10).until(
            EC.url_contains("/payment")
        )
        
        # Check booking summary
        booking_summary = logged_in_user.find_element(By.ID, "booking-summary")
        assert "2 hours" in booking_summary.text
    
    def test_booking_conflict(self, logged_in_user):
        """Test booking time conflict"""
        
        logged_in_user.get("http://localhost:3000/spaces")
        
        # Try to book already reserved time slot
        first_space = logged_in_user.find_element(By.CLASS_NAME, "book-btn")
        first_space.click()
        
        # Fill with conflicting time
        date_input = logged_in_user.find_element(By.ID, "booking-date")
        date_input.send_keys("2024-12-24")  # Assume this date has conflicts
        
        start_time = Select(logged_in_user.find_element(By.ID, "start-time"))
        start_time.select_by_value("10:00")
        
        end_time = Select(logged_in_user.find_element(By.ID, "end-time"))
        end_time.select_by_value("12:00")
        
        logged_in_user.find_element(By.ID, "confirm-booking-btn").click()
        
        # Check for conflict error
        error_message = WebDriverWait(logged_in_user, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
        )
        assert "Time slot not available" in error_message.text
    
    def test_booking_calendar_view(self, logged_in_user):
        """Test calendar view for bookings"""
        
        logged_in_user.get("http://localhost:3000/spaces/1")
        
        # Switch to calendar view
        calendar_btn = logged_in_user.find_element(By.ID, "calendar-view-btn")
        calendar_btn.click()
        
        # Wait for calendar to load
        WebDriverWait(logged_in_user, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "calendar"))
        )
        
        # Check that calendar shows available/unavailable slots
        calendar_slots = logged_in_user.find_elements(By.CLASS_NAME, "time-slot")
        assert len(calendar_slots) > 0
        
        # Check that some slots are marked as unavailable
        unavailable_slots = logged_in_user.find_elements(By.CLASS_NAME, "slot-unavailable")
        available_slots = logged_in_user.find_elements(By.CLASS_NAME, "slot-available")
        
        assert len(available_slots) > 0 or len(unavailable_slots) > 0