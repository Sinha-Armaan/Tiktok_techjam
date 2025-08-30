# Regional Content Management - Gray Area Case
import datetime
from typing import Dict, List

class RegionalContentManager:
    """Manages content availability by region - purpose unclear"""
    
    def __init__(self):
        # Geographic restrictions but reasons are vague
        self.content_policies = {
            "US": {
                "blocked_categories": ["political_ads"],  # Election laws?
                "age_restrictions": {"min_age": 13},  # COPPA?
                "moderation_level": "standard"
            },
            "EU": {
                "data_subject_rights": True,  # GDPR?
                "algorithm_transparency": True,  # DSA?
                "content_labeling": "required"
            },
            "CA": {
                "privacy_controls": True,  # California privacy laws?
                "minor_protections": True,  # New CA social media laws?
                "addiction_controls": True
            },
            "FL": {
                "parental_verification": True,  # Florida minor protection?
                "social_media_restrictions": True
            }
        }
    
    def check_content_availability(self, content_id: str, user_region: str, user_age: int):
        """Check if content is available - compliance vs business logic unclear"""
        
        if user_region not in self.content_policies:
            # Default behavior - might not be compliant
            return {"available": True, "restrictions": None}
        
        policy = self.content_policies[user_region]
        restrictions = []
        
        # Age-based restrictions (could be legal compliance)
        if user_age < policy.get("age_restrictions", {}).get("min_age", 0):
            restrictions.append("age_restricted")
            # But is this actual COPPA compliance or just business policy?
        
        # Regional content blocking (legal or business?)
        if self.is_blocked_content(content_id, policy):
            restrictions.append("regionally_blocked")
        
        # Parental controls (legal requirement or feature?)
        if policy.get("parental_verification") and user_age < 18:
            if not self.has_parental_consent(user_region, user_age):
                restrictions.append("requires_parental_consent")
        
        needs_review = len(restrictions) > 0 and user_region in ["CA", "FL", "EU"]
        
        return {
            "available": len(restrictions) == 0,
            "restrictions": restrictions,
            "compliance_uncertain": needs_review,  # Gray area flag
            "region": user_region
        }
    
    def is_blocked_content(self, content_id: str, policy: Dict):
        """Check if content is blocked - unclear if legal or business"""
        # This logic could be copyright compliance, election laws, or business decisions
        blocked_categories = policy.get("blocked_categories", [])
        
        # Simulated content categorization
        content_category = self.get_content_category(content_id)
        return content_category in blocked_categories
    
    def get_content_category(self, content_id: str):
        """Categorize content - simplified for demo"""
        # Mock categorization
        categories = ["entertainment", "political_ads", "news", "educational"]
        return categories[hash(content_id) % len(categories)]
    
    def has_parental_consent(self, region: str, user_age: int):
        """Check parental consent - implementation unclear"""
        # This is a gray area - is the consent mechanism legally sufficient?
        if user_age >= 18:
            return True
        
        # Mock consent check - might not meet legal standards
        consent_mechanisms = {
            "US": "email_verification",  # Is this sufficient for COPPA?
            "CA": "identity_verification",  # Meets new CA requirements?
            "FL": "parent_id_check",  # Complies with FL law?
            "EU": "gdpr_consent_flow"  # Actually GDPR compliant?
        }
        
        mechanism = consent_mechanisms.get(region, "basic_check")
        # Return uncertain status - needs human review
        return mechanism in ["identity_verification", "parent_id_check"]

class DataRetentionManager:
    """Manages data retention - compliance status unclear"""
    
    def __init__(self):
        # Different retention periods by region - legal or business?
        self.retention_policies = {
            "EU": {"days": 30, "reason": "gdpr_compliance"},  # Is 30 days correct?
            "CA": {"days": 90, "reason": "ccpa_compliance"},  # CCPA requirements?
            "BR": {"days": 365, "reason": "lgpd_compliance"},  # LGPD rules?
            "US": {"days": 730, "reason": "business_policy"},  # No specific law
            "default": {"days": 1095, "reason": "standard_retention"}
        }
    
    def get_retention_period(self, user_region: str, data_type: str):
        """Get retention period - legal accuracy uncertain"""
        policy = self.retention_policies.get(user_region, self.retention_policies["default"])
        
        # Special cases that might need legal review
        if data_type == "biometric" and user_region == "US":
            # Illinois BIPA or other state biometric laws?
            return {"days": 180, "reason": "biometric_law_compliance", "uncertain": True}
        
        if data_type == "child_data" and user_region in ["US", "EU"]:
            # COPPA or GDPR Article 8?
            return {"days": 30, "reason": "minor_protection", "uncertain": True}
        
        return {
            "days": policy["days"],
            "reason": policy["reason"],
            "uncertain": policy["reason"].endswith("_compliance")  # Flag for review
        }
    
    def schedule_data_deletion(self, user_id: str, region: str, data_types: List[str]):
        """Schedule deletion - implementation might not be legally sufficient"""
        deletion_schedule = []
        
        for data_type in data_types:
            retention = self.get_retention_period(region, data_type)
            
            deletion_date = datetime.datetime.now() + datetime.timedelta(days=retention["days"])
            
            deletion_schedule.append({
                "user_id": user_id,
                "data_type": data_type,
                "deletion_date": deletion_date.isoformat(),
                "legal_basis": retention["reason"],
                "needs_review": retention.get("uncertain", False)
            })
        
        return {
            "scheduled_deletions": deletion_schedule,
            "total_items": len(deletion_schedule),
            "compliance_status": "uncertain" if any(item["needs_review"] for item in deletion_schedule) else "assumed_compliant"
        }
