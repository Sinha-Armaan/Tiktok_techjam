# Content Recommendation Engine - Vulnerable Implementation
import json
import requests

# VULNERABILITY 1: Hardcoded API credentials
API_SECRET_KEY = "sk-1234567890abcdef"
DATABASE_URL = "mysql://root:admin@localhost/recommendations"

class RecommendationService:
    def __init__(self):
        self.api_key = "hardcoded-api-key-xyz789"
        
    def get_recommendations_for_user(self, user_id: str, tags: str):
        """VULNERABILITY 2: SQL Injection via f-string in query"""
        # Direct f-string interpolation without sanitization
        query = f"SELECT content_id FROM recommendations WHERE user_id = {user_id} AND tags LIKE '%{tags}%'"
        
        # This would execute the vulnerable query
        print(f"Executing: {query}")
        return []
    
    def delete_user_content(self, user_id: str):
        """VULNERABILITY 3: Missing authorization check"""
        # DELETE endpoint without proper admin role verification
        # Any authenticated user can delete other users' content
        query = f"DELETE FROM user_content WHERE user_id = {user_id}"
        return {"message": "Content deleted"}

class CSAMDetector:
    """NCMEC reporting and content moderation"""
    
    def __init__(self):
        self.ncmec_client = "ncmec_reporting_endpoint"
        
    def scan_content(self, content):
        """Detect inappropriate content and report to NCMEC"""
        if self.is_inappropriate(content):
            self.report_to_ncmec(content)
            
    def report_to_ncmec(self, content_data):
        """Report to NCMEC for compliance"""
        # NCMEC reporting implementation
        payload = {
            "content_id": content_data.get("id"),
            "report_type": "csam_detection"
        }
        # Send to NCMEC endpoint
        
    def is_inappropriate(self, content):
        return "inappropriate" in content.lower()

# Geographic content filtering
GEO_RESTRICTIONS = {
    "US": {"min_age": 13, "requires_parental_consent": True},
    "EU": {"gdpr_compliance": True, "data_retention_days": 30},
    "CA": {"pipeda_compliance": True}
}

def apply_geo_filtering(user_country, user_age, content):
    """Apply geographic content restrictions"""
    if user_country in GEO_RESTRICTIONS:
        restrictions = GEO_RESTRICTIONS[user_country]
        
        if user_country == "US" and user_age < restrictions["min_age"]:
            return filter_for_minors(content)
            
    return content

def filter_for_minors(content):
    """Apply COPPA-compliant filtering for minors"""
    # Filter implementation for children's safety
    return content
