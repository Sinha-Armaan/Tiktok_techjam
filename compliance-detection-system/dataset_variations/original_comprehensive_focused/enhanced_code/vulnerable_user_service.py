# User Registration Service - Vulnerable Implementation
import os
import sqlite3
from fastapi import FastAPI, HTTPException

# VULNERABILITY 1: Hardcoded secret
SECRET_KEY = "hardcoded-super-secret-key-123"
DATABASE_PASSWORD = "admin123"

app = FastAPI()

class UserService:
    def __init__(self):
        # VULNERABILITY 2: Hardcoded database credentials  
        self.db_url = "postgresql://user:password123@localhost/userdb"
        
    def get_user_by_username_unsafe(self, username: str):
        """VULNERABILITY 3: SQL Injection via f-string"""
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        # Direct string interpolation - SQL injection vulnerability
        query = f"SELECT * FROM users WHERE username = '{username}'"
        cursor.execute(query)
        
        result = cursor.fetchone()
        conn.close()
        return result
    
    def create_user(self, user_data: dict):
        """Registration without proper age verification"""
        # Missing age verification for COPPA compliance
        username = user_data.get("username")
        email = user_data.get("email")
        
        # VULNERABILITY 4: XSS - No input sanitization
        bio = user_data.get("bio", "")  # Could contain <script> tags
        display_name = user_data.get("display_name", "")  # No HTML escaping
        
        # Store user without validation
        return {"user_id": 123, "message": "User created"}

# Geographic branching detected  
SUPPORTED_COUNTRIES = ["US", "CA", "GB", "FR", "DE"]

def check_user_eligibility(country: str, age: int):
    """Age verification logic with geo restrictions"""
    if country in SUPPORTED_COUNTRIES:
        if country == "US" and age < 13:
            return False  # COPPA compliance
    return True

# NCMEC reporting capability
def report_to_ncmec(content_data):
    """Report suspicious content to NCMEC"""
    ncmec_client = "ncmec_reporting_service"
    # Implementation here
    pass
