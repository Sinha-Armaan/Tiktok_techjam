"""
User Registration Service

This module handles user registration, age verification, and geographic restrictions.
"""

import datetime
from typing import Optional, Dict, List
from dataclasses import dataclass

# Geographic restrictions configuration
SUPPORTED_COUNTRIES = ['US', 'CA', 'GB', 'FR', 'DE', 'IT', 'ES', 'AU', 'JP']
BLOCKED_COUNTRIES = ['CN', 'RU', 'KP']

# Utah-specific compliance requirements
UT_CURFEW_HOURS = {
    'start': '22:30',  # 10:30 PM
    'end': '06:30'     # 6:30 AM
}

@dataclass
class UserLocation:
    country: str
    state: Optional[str] = None
    city: Optional[str] = None


class AgeVerificationService:
    """Handles age verification for compliance with various regulations"""
    
    def __init__(self):
        from age_gate import verify_age
        self.age_verifier = verify_age
        
    def verify_user_age(self, birth_date: datetime.date) -> Dict[str, bool]:
        """Verify user age against various thresholds"""
        today = datetime.date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        return {
            'is_coppa_age': age < 13,      # COPPA threshold
            'is_minor': age < 18,          # General minor threshold
            'is_utah_minor': age < 18,     # Utah specific
            'requires_parental_consent': age < 13,
            'age_verified': True
        }


class GeographicComplianceService:
    """Handles geographic-based compliance requirements"""
    
    def __init__(self):
        self.data_residency_regions = {
            'US': 'us-east',
            'CA': 'us-east', 
            'GB': 'eu-west',
            'FR': 'eu-west',
            'DE': 'eu-west',
            'AU': 'asia-pacific'
        }
    
    def check_geographic_restrictions(self, location: UserLocation, user_age: int) -> Dict[str, bool]:
        """Check various geographic compliance requirements"""
        restrictions = {
            'country_allowed': location.country in SUPPORTED_COUNTRIES,
            'country_blocked': location.country in BLOCKED_COUNTRIES,
            'requires_gdpr_compliance': location.country in ['GB', 'FR', 'DE', 'IT', 'ES'],
            'requires_utah_restrictions': location.state == 'UT' and user_age < 18,
            'requires_coppa_compliance': location.country == 'US' and user_age < 13
        }
        
        return restrictions
    
    def get_data_region(self, country: str) -> str:
        """Get data residency region for country"""
        return self.data_residency_regions.get(country, 'us-east')


class UserRegistrationService:
    """Main user registration service with compliance features"""
    
    def __init__(self):
        self.age_service = AgeVerificationService()
        self.geo_service = GeographicComplianceService()
        self.parental_consent_required = False
        
    def register_user(self, user_data: Dict) -> Dict[str, any]:
        """Register new user with compliance checks"""
        location = UserLocation(
            country=user_data.get('country', 'US'),
            state=user_data.get('state')
        )
        
        # Age verification
        birth_date = user_data.get('birth_date')
        age_check = self.age_service.verify_user_age(birth_date)
        
        # Geographic compliance
        geo_check = self.geo_service.check_geographic_restrictions(
            location, 
            self._calculate_age(birth_date)
        )
        
        # Determine data storage region
        storage_region = self.geo_service.get_data_region(location.country)
        
        result = {
            'registration_allowed': geo_check['country_allowed'] and not geo_check['country_blocked'],
            'age_verification': age_check,
            'geographic_compliance': geo_check,
            'data_region': storage_region,
            'parental_consent_required': age_check['requires_parental_consent'],
            'utah_minor_restrictions': geo_check['requires_utah_restrictions']
        }
        
        return result
    
    def _calculate_age(self, birth_date: datetime.date) -> int:
        """Calculate age from birth date"""
        today = datetime.date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


# Feature flags for compliance
FEATURE_FLAG_COMPLIANCE_UTAH_MINORS = True
FEATURE_FLAG_COMPLIANCE_GDPR_MODE = True
FEATURE_FLAG_COMPLIANCE_COPPA_STRICT = True
