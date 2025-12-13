from locust import HttpUser, task, between
import json
import random

class CoworkFlowUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Setup user session"""
        self.signup_and_login()
    
    def signup_and_login(self):
        """Register and login user"""
        user_id = random.randint(1000, 9999)
        self.email = f"loadtest{user_id}@example.com"
        self.password = "loadtest123"
        
        # Signup
        signup_data = {
            "email": self.email,
            "password": self.password,
            "name": f"Load Test User {user_id}",
            "role": "user"
        }
        self.client.post("/auth/signup", json=signup_data)
        
        # Login
        login_data = {"email": self.email, "password": self.password}
        response = self.client.post("/auth/login", json=login_data)
        
        if response.status_code == 200:
            self.token = response.json().get("token")
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = None
            self.headers = {}
    
    @task(3)
    def view_spaces(self):
        """View available spaces"""
        self.client.get("/spaces")
    
    @task(2)
    def view_space_details(self):
        """View specific space details"""
        space_id = random.randint(1, 10)
        self.client.get(f"/spaces/{space_id}")
    
    @task(1)
    def create_reservation(self):
        """Create a new reservation"""
        if not self.token:
            return
            
        reservation_data = {
            "space_id": random.randint(1, 5),
            "start_time": "2024-12-25T10:00:00",
            "end_time": "2024-12-25T12:00:00"
        }
        
        self.client.post("/reservations", 
                        json=reservation_data, 
                        headers=self.headers)
    
    @task(2)
    def view_my_reservations(self):
        """View user's reservations"""
        if not self.token:
            return
            
        self.client.get("/reservations/user/me", headers=self.headers)
    
    @task(1)
    def calculate_pricing(self):
        """Calculate pricing for booking"""
        pricing_data = {
            "space_id": random.randint(1, 5),
            "hours": random.randint(1, 8),
            "user_type": "regular"
        }
        
        self.client.post("/pricing/calc", json=pricing_data)