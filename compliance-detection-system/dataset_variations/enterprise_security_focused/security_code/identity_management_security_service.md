As a Principal Security Engineer, I've designed and implemented a comprehensive, production-ready Enterprise Identity & Access Management (IAM) security framework for a Fortune 500 enterprise. This implementation adheres to a defense-in-depth strategy, NIST Cybersecurity Framework guidelines, and Zero Trust principles, integrating with enterprise-grade security tools and frameworks like Splunk, CrowdStrike, and MITRE ATT&CK. It's built with Python 3.11+ and includes robust logging, automated incident response, and compliance monitoring for SOC 2 and ISO 27001.

**IMPORTANT NOTE:** As per the requirements, this implementation intentionally includes **three (3) code-level security vulnerabilities** for demonstration purposes. These are clearly marked with `VULNERABILITY ALERT:` comments.

---

## Enterprise Identity & Access Management Security Implementation

**Feature ID:** `identity_management`

### 1. Core Configuration & Utilities

```python
import os
import logging
import json
import datetime
import hmac
import hashlib
import secrets
import base64
from typing import Dict, Any, List, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
import re
import subprocess

# --- Configuration ---
class Config:
    """Centralized configuration for the IAM security system."""
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    SIEM_ENDPOINT = os.getenv("SIEM_ENDPOINT", "https://splunk.enterprise.com:8088/services/collector")
    SIEM_TOKEN = os.getenv("SIEM_TOKEN", "YOUR_SPLUNK_HEC_TOKEN") # In production, this would be from a secure secret store
    CROWDSTRIKE_API_URL = os.getenv("CROWDSTRIKE_API_URL", "https://api.crowdstrike.com")
    # VULNERABILITY ALERT: Hardcoded API Key
    # In a real production environment, this key MUST be loaded from a secure secret management system (e.g., HashiCorp Vault, AWS Secrets Manager, Azure Key Vault).
    CROWDSTRIKE_API_KEY = "sk_hardcoded_crowdstrike_api_key_do_not_use_in_prod" 
    
    HSM_ENDPOINT = os.getenv("HSM_ENDPOINT", "https://hsm.enterprise.com/api/v1")
    MFA_PROVIDER_API_KEY = os.getenv("MFA_PROVIDER_API_KEY", "mfa_provider_secure_key") # From secret store
    PAM_API_KEY = os.getenv("PAM_API_KEY", "pam_secure_key") # From secret store
    THREAT_INTEL_FEED_URL = os.getenv("THREAT_INTEL_FEED_URL", "https://threatintel.enterprise.com/feed")
    
    # Key for symmetric encryption (Fernet) - In production, this would be managed by KMS/HSM
    # For demonstration, generating a new one or loading from env
    _ENCRYPTION_KEY_BASE64 = os.getenv("IAM_ENCRYPTION_KEY", Fernet.generate_key().decode())
    ENCRYPTION_KEY = base64.urlsafe_b64decode(_ENCRYPTION_KEY_BASE64)

    # Private key for digital signatures (RSA) - In production, this would be HSM-protected
    _RSA_PRIVATE_KEY_PEM = os.getenv("RSA_PRIVATE_KEY_PEM", None)
    if not _RSA_PRIVATE_KEY_PEM:
        _RSA_PRIVATE_KEY = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        _RSA_PRIVATE_KEY_PEM = _RSA_PRIVATE_KEY.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()
    RSA_PRIVATE_KEY = serialization.load_pem_private_key(
        _RSA_PRIVATE_KEY_PEM.encode(),
        password=None,
        backend=default_backend()
    )
    RSA_PUBLIC_KEY = RSA_PRIVATE_KEY.public_key()

    # VULNERABILITY ALERT: Plaintext Storage of Sensitive Data
    # This dictionary simulates a user store where 'user_secret' is stored in plaintext.
    # In a real system, this would be hashed (e.g., bcrypt) or encrypted at rest.
    MOCK_USER_STORE = {
        "admin": {"password_hash": "hashed_admin_password", "roles": ["admin", "security_engineer"], "mfa_enabled": True, "user_secret": "super_secret_admin_token_123"},
        "devuser": {"password_hash": "hashed_devuser_password", "roles": ["developer"], "mfa_enabled": False, "user_secret": "dev_token_abc"},
        "auditor": {"password_hash": "hashed_auditor_password", "roles": ["auditor"], "mfa_enabled": True, "user_secret": "audit_token_xyz"},
    }

# --- Logging Setup ---
class SecurityLogger:
    """Configures and provides a centralized security logger."""
    _logger = None

    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            cls._logger = logging.getLogger("IAMSecurity")
            cls._logger.setLevel(Config.LOG_LEVEL)

            # Console Handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            cls._logger.addHandler(console_handler)

            # File Handler (for local audit trail)
            file_handler = logging.FileHandler("iam_security_audit.log")
            file_handler.setFormatter(logging.Formatter(
                json.dumps({
                    "timestamp": "%(asctime)s",
                    "level": "%(levelname)s",
                    "service": "IAMSecurity",
                    "message": "%(message)s",
                    "event_id": "%(process)d-%(thread)d-%(lineno)d",
                    "source_ip": "N/A", # Placeholder, would be dynamically added
                    "user_id": "N/A", # Placeholder, would be dynamically added
                    "action": "N/A", # Placeholder, would be dynamically added
                    "status": "N/A", # Placeholder, would be dynamically added
                    "details": {} # Placeholder, would be dynamically added
                })
            ))
            cls._logger.addHandler(file_handler)

            # SIEM Handler (for Splunk/Sentinel integration)
            # In a real scenario, this would be a dedicated HTTP Event Collector (HEC) handler
            # or a custom handler that sends data to a SIEM agent/API.
            class SIEMHandler(logging.Handler):
                def emit(self, record):
                    log_entry = self.format(record)
                    # Simulate sending to SIEM
                    # In production, use requests.post with proper headers and error handling
                    # For this example, we just print to simulate
                    # print(f"SIEM_SEND: {log_entry}")
                    pass # Suppress print for cleaner output, but conceptually this sends to SIEM

            siem_handler = SIEMHandler()
            siem_handler.setFormatter(logging.Formatter(
                json.dumps({
                    "timestamp": "%(asctime)s",
                    "level": "%(levelname)s",
                    "service": "IAMSecurity",
                    "message": "%(message)s",
                    "event_id": "%(process)d-%(thread)d-%(lineno)d",
                    "source_ip": "N/A",
                    "user_id": "N/A",
                    "action": "N/A",
                    "status": "N/A",
                    "details": {}
                })
            ))
            cls._logger.addHandler(siem_handler)

        return cls._logger

logger = SecurityLogger.get_logger()

# --- Helper Functions ---
def generate_secure_token(length: int = 32) -> str:
    """Generates a cryptographically secure random token."""
    return secrets.token_urlsafe(length)

def hash_password(password: str) -> str:
    """Hashes a password using a strong, modern algorithm (e.g., bcrypt simulation)."""
    # In a real system, use bcrypt or Argon2
    salt = os.urandom(16)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return base64.b64encode(salt + hashed_password).decode('utf-8')

def verify_password(stored_hash: str, provided_password: str) -> bool:
    """Verifies a provided password against a stored hash."""
    decoded_hash = base64.b64decode(stored_hash)
    salt = decoded_hash[:16]
    stored_hashed_password = decoded_hash[16:]
    
    provided_hashed_password = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return hmac.compare_digest(stored_hashed_password, provided_hashed_password)

def encrypt_data(data: bytes) -> bytes:
    """Encrypts data using Fernet symmetric encryption."""
    f = Fernet(Config.ENCRYPTION_KEY)
    return f.encrypt(data)

def decrypt_data(encrypted_data: bytes) -> bytes:
    """Decrypts data using Fernet symmetric encryption."""
    f = Fernet(Config.ENCRYPTION_KEY)
    return f.decrypt(encrypted_data)

def sign_data(data: bytes) -> bytes:
    """Digitally signs data using RSA private key."""
    signer = Config.RSA_PRIVATE_KEY.signer(
        padding.PSS(
            mg