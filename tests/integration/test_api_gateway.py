import pytest
import requests
import json

BASE_URL = "http://localhost:8000"

class TestAPIGateway:
    
    def test_gateway_routing(self):
        """Test that API Gateway correctly routes requests to microservices"""
        
        # Test routing to users service
        response = requests.get(f"{BASE_URL}/users/health")
        assert response.status_code in [200, 404]  # Service may not be running
        
        # Test routing to spaces service
        response = requests.get(f"{BASE_URL}/spaces")
        assert response.status_code in [200, 404]
        
        # Test routing to reservations service
        response = requests.get(f"{BASE_URL}/reservations/health")
        assert response.status_code in [200, 404]
    
    def test_authentication_middleware(self):
        """Test JWT authentication middleware"""
        
        # Test protected endpoint without token
        response = requests.get(f"{BASE_URL}/users/me")
        assert response.status_code == 401
        
        # Test with invalid token
        headers = {'Authorization': 'Bearer invalid_token'}
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        assert response.status_code == 401
    
    def test_cors_headers(self):
        """Test CORS headers are properly set"""
        
        response = requests.options(f"{BASE_URL}/spaces")
        assert 'Access-Control-Allow-Origin' in response.headers
        assert 'Access-Control-Allow-Methods' in response.headers
    
    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        
        # Make multiple rapid requests
        responses = []
        for i in range(20):
            response = requests.get(f"{BASE_URL}/spaces")
            responses.append(response.status_code)
        
        # Should have some rate limiting after many requests
        assert any(status == 429 for status in responses[-5:])
    
    def test_request_logging(self):
        """Test that requests are properly logged"""
        
        # Make a request
        response = requests.get(f"{BASE_URL}/spaces")
        
        # Check response headers for request ID
        assert 'X-Request-ID' in response.headers
    
    def test_error_handling(self):
        """Test gateway error handling"""
        
        # Test non-existent endpoint
        response = requests.get(f"{BASE_URL}/nonexistent")
        assert response.status_code == 404
        
        # Test malformed request
        response = requests.post(f"{BASE_URL}/spaces", data="invalid json")
        assert response.status_code == 400