# Dataset Variations Directory

This directory contains all the dataset variations for the compliance detection system, each focused on different aspects of compliance and security testing.

## 📁 Directory Structure

### 🔧 Original Comprehensive Focused (`original_comprehensive_focused/`)
**Theme**: General compliance detection with comprehensive feature coverage

**Focus Areas**:
- User registration compliance (COPPA, GDPR)
- Content recommendation systems
- Crisis intervention mechanisms
- General privacy and data protection

**Generator**: `generate_original_datasets.py`

**Key Features**:
- Comprehensive PRDs, TRDs, and implementation code
- AI-enhanced artifacts with intentional compliance gaps
- Multi-faceted compliance testing scenarios

---

### 🔒 Enterprise Security Focused (`enterprise_security_focused/`)
**Theme**: Advanced cybersecurity and enterprise-grade security features

**Focus Areas**:
- Advanced threat detection systems with MITRE ATT&CK integration
- Zero Trust architecture implementation  
- Enterprise identity & access management (IAM)
- Real-time security monitoring & SIEM integration
- Compliance frameworks (NIST, SOC 2, ISO 27001)

**Generator**: `generate_security_datasets.py`

**Key Features**:
- Security-focused PRDs and TRDs with intentional security gaps
- Enterprise-grade security implementations with vulnerabilities
- CISO-level security documentation with compliance oversights

---

### 🌍 Global Expansion Focused (`global_expansion_focused/`)
**Theme**: International compliance and multi-region operations

**Focus Areas**:
- Multi-region data compliance (GDPR, CCPA, PIPEDA, LGPD)
- Content localization & internationalization (i18n) engines
- Cross-border data transfer management
- Regional content moderation with cultural adaptation
- Data sovereignty and localization strategies

**Generator**: `generate_global_datasets.py`

**Key Features**:
- Global compliance PRDs and TRDs with regulatory gaps
- International expansion implementation with privacy oversights
- Cultural adaptation and localization with compliance issues

---

## 🎯 Intentional Issues Included

All generators have been configured to include **intentional compliance and security issues** for testing:

### 📋 PRD-Level Issues:
- Missing age verification or COPPA compliance gaps
- Inadequate data retention/deletion policies
- Missing consent management details
- Insufficient privacy disclosures
- Unclear data sharing policies
- Missing accessibility compliance (WCAG)

### 🔧 TRD-Level Issues:
- Missing input validation or SQL injection vulnerabilities
- Weak authentication/authorization mechanisms
- Insecure data handling practices
- Missing rate limiting or DOS protection
- Inadequate error handling exposing sensitive data
- Poor logging or audit trail implementation

### 💻 Code-Level Issues:
- Hardcoded secrets, API keys, passwords
- SQL injection vulnerabilities
- Missing input validation (XSS/injection attacks)
- Insecure HTTP connections
- Poor error handling exposing system info
- Missing authentication on sensitive endpoints
- Weak encryption or plaintext PII storage

---

## 🚀 Usage Instructions

To generate a specific dataset variation:

```bash
# Original comprehensive focused
cd original_comprehensive_focused
python generate_original_datasets.py

# Enterprise security focused  
cd enterprise_security_focused
python generate_security_datasets.py

# Global expansion focused
cd global_expansion_focused
python generate_global_datasets.py
```

Each generator will create:
- 📊 **Core datasets** (CSV, JSON, YAML files)
- 📄 **Enhanced artifacts** (PRDs, TRDs, design docs)
- 💻 **Implementation code** (Python services with intentional issues)

---

## 📊 Generated Artifacts Summary

| Variation | PRDs | TRDs | Code Files | Design Docs | Additional |
|-----------|------|------|------------|-------------|------------|
| Original | 3 | 3 | 3 | 3 | Test cases, user stories, risk assessments |
| Security | 4 | 4 | 4 | 3 | Security policies, compliance matrix, test cases |
| Global | 4 | 4 | 4 | 3 | Cultural guides, market entry playbooks, compliance checklists |

---

## 🎯 Testing Your Compliance Detection System

These datasets provide comprehensive test data for validating your compliance detection algorithms across:

✅ **Product Management** - PRDs with compliance gaps  
✅ **Technical Architecture** - TRDs with security oversights  
✅ **Code Implementation** - Services with actual vulnerabilities  
✅ **Multiple Domains** - General, security-focused, and international scenarios  

Perfect for testing automated compliance scanning, security vulnerability detection, and regulatory gap analysis!
