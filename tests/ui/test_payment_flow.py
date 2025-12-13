import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

class TestPaymentFlow:
    
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
    def user_with_booking(self, driver):
        """Setup user with a pending booking"""
        # Login
        driver.get("http://localhost:3000/login")
        driver.find_element(By.ID, "email").send_keys("test@example.com")
        driver.find_element(By.ID, "password").send_keys("password123")
        driver.find_element(By.ID, "login-btn").click()
        
        # Create a booking (navigate to payment page)
        driver.get("http://localhost:3000/payment/booking123")
        return driver
    
    def test_credit_card_payment(self, user_with_booking):
        """Test successful credit card payment"""
        
        # Select credit card payment method
        card_radio = user_with_booking.find_element(By.ID, "payment-card")
        card_radio.click()
        
        # Fill card details
        user_with_booking.find_element(By.ID, "card-number").send_keys("4111111111111111")
        user_with_booking.find_element(By.ID, "card-name").send_keys("Test User")
        user_with_booking.find_element(By.ID, "card-expiry").send_keys("12/25")
        user_with_booking.find_element(By.ID, "card-cvv").send_keys("123")
        
        # Submit payment
        user_with_booking.find_element(By.ID, "pay-btn").click()
        
        # Wait for success page
        WebDriverWait(user_with_booking, 15).until(
            EC.url_contains("/payment/success")
        )
        
        # Check success message
        success_message = user_with_booking.find_element(By.CLASS_NAME, "payment-success")
        assert "Payment successful" in success_message.text
        
        # Check booking confirmation
        booking_details = user_with_booking.find_element(By.ID, "booking-confirmation")
        assert "confirmed" in booking_details.text.lower()
    
    def test_pix_payment(self, user_with_booking):
        """Test PIX payment flow"""
        
        # Select PIX payment method
        pix_radio = user_with_booking.find_element(By.ID, "payment-pix")
        pix_radio.click()
        
        # Submit PIX payment
        user_with_booking.find_element(By.ID, "pay-btn").click()
        
        # Wait for PIX QR code page
        WebDriverWait(user_with_booking, 10).until(
            EC.presence_of_element_located((By.ID, "pix-qr-code"))
        )
        
        # Check PIX code is displayed
        pix_code = user_with_booking.find_element(By.ID, "pix-code")
        assert len(pix_code.text) > 0
        
        # Check QR code image is present
        qr_image = user_with_booking.find_element(By.ID, "pix-qr-code")
        assert qr_image.get_attribute("src")
        
        # Check payment instructions
        instructions = user_with_booking.find_element(By.CLASS_NAME, "pix-instructions")
        assert "scan the QR code" in instructions.text.lower()
    
    def test_invalid_card_details(self, user_with_booking):
        """Test payment with invalid card details"""
        
        # Select credit card
        card_radio = user_with_booking.find_element(By.ID, "payment-card")
        card_radio.click()
        
        # Fill invalid card details
        user_with_booking.find_element(By.ID, "card-number").send_keys("1234567890123456")  # Invalid
        user_with_booking.find_element(By.ID, "card-name").send_keys("Test User")
        user_with_booking.find_element(By.ID, "card-expiry").send_keys("01/20")  # Expired
        user_with_booking.find_element(By.ID, "card-cvv").send_keys("12")  # Invalid CVV
        
        user_with_booking.find_element(By.ID, "pay-btn").click()
        
        # Check for error message
        error_message = WebDriverWait(user_with_booking, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "payment-error"))
        )
        assert "payment failed" in error_message.text.lower()
    
    def test_payment_summary(self, user_with_booking):
        """Test payment summary display"""
        
        # Check booking summary is displayed
        summary = user_with_booking.find_element(By.ID, "payment-summary")
        assert summary.is_displayed()
        
        # Check required summary elements
        space_name = user_with_booking.find_element(By.CLASS_NAME, "summary-space")
        assert len(space_name.text) > 0
        
        date_time = user_with_booking.find_element(By.CLASS_NAME, "summary-datetime")
        assert len(date_time.text) > 0
        
        total_amount = user_with_booking.find_element(By.CLASS_NAME, "summary-total")
        assert "R$" in total_amount.text or "$" in total_amount.text
    
    def test_payment_timeout(self, user_with_booking):
        """Test payment timeout handling"""
        
        # Select PIX payment
        pix_radio = user_with_booking.find_element(By.ID, "payment-pix")
        pix_radio.click()
        
        user_with_booking.find_element(By.ID, "pay-btn").click()
        
        # Wait for PIX page
        WebDriverWait(user_with_booking, 10).until(
            EC.presence_of_element_located((By.ID, "pix-timer"))
        )
        
        # Check timer is displayed
        timer = user_with_booking.find_element(By.ID, "pix-timer")
        assert timer.is_displayed()
        
        # Check timeout message appears (simulate or check initial state)
        timeout_info = user_with_booking.find_element(By.CLASS_NAME, "timeout-info")
        assert "expires in" in timeout_info.text.lower()