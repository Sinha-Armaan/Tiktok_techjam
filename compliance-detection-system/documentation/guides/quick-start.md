# Quick Start Guide

Get the **Compliance Detection System (CDS)** up and running in under 10 minutes with our demo pipeline.

## ✅ Prerequisites Checklist

Before starting, verify you have:

- [ ] **Python 3.11+** installed
  ```powershell
  python --version  # Should show 3.11.0 or higher
  ```

- [ ] **Git** for repository operations
  ```powershell
  git --version
  ```

- [ ] **Google AI Studio Account** for LLM analysis
  - Create a free account at [Google AI Studio](https://aistudio.google.com/)
  - Generate an API key (instructions in Step 2 below)

- [ ] **Virtual environment** support (built into Python 3.11+)
- [ ] **Internet connection** for package downloads and API calls

### Optional (for advanced functionality):
- [ ] **Google Cloud Account** with [Vertex AI API enabled](https://console.cloud.google.com/apis/library/aiplatform.googleapis.com)
- [ ] **Docker** for containerized deployment (optional)

## 🚀 5-Minute Demo

### Step 1: Clone and Setup

```powershell
# Clone the repository
git clone https://github.com/your-org/compliance-detection-system.git
cd compliance-detection-system

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -e .
```

### Step 2: Configure Environment

```powershell
# Copy the environment template
copy .env.example .env

# Edit the .env file with your API keys
notepad .env
```

**Required Configuration:**
```ini
# Google AI Studio API (Required for LLM analysis)
GOOGLE_API_KEY=your_google_ai_studio_api_key_here

# Optional: Vertex AI (alternative to Google AI Studio)
# GOOGLE_CLOUD_PROJECT=your-project-id
# GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# LLM Model Configuration
GEMINI_MODEL=gemini-2.0-flash-exp
```

**🔑 Getting Your Google AI Studio API Key:**
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key" → "Create API Key"
4. Copy the key and paste it in your `.env` file

### Step 3: Verify Installation

```powershell
# Test CLI is working
cds --help

# Expected output:
# Usage: cds [OPTIONS] COMMAND [ARGS]...
# 
# Compliance Detection System - Detect geo-specific compliance requirements
```

### Step 4: Generate Evidence Files

Before running the pipeline, generate evidence files from the comprehensive dataset artifacts:

```powershell
# Generate evidence files for all dataset variations
python generate_evidence.py
```

**Expected Output:**
```
🔍 Evidence Generator for Dataset Variations
============================================================
🔍 Creating evidence files for original_comprehensive_focused...
📋 Loaded 3 features from original_comprehensive_focused
✅ Created evidence: artifacts\evidence\user_registration.json
✅ Created evidence: artifacts\evidence\content_recommendation.json
✅ Created evidence: artifacts\evidence\crisis_intervention.json

🔍 Creating evidence files for enterprise_security_focused...
📋 Loaded 4 features from enterprise_security_focused
✅ Created evidence: artifacts\evidence\threat_detection.json
✅ Created evidence: artifacts\evidence\zero_trust_architecture.json
✅ Created evidence: artifacts\evidence\identity_management.json
✅ Created evidence: artifacts\evidence\security_monitoring.json

🔍 Creating evidence files for global_expansion_focused...
📋 Loaded 4 features from global_expansion_focused
✅ Created evidence: artifacts\evidence\multi_region_compliance.json
✅ Created evidence: artifacts\evidence\localization_engine.json
✅ Created evidence: artifacts\evidence\cross_border_transfers.json
✅ Created evidence: artifacts\evidence\regional_content_moderation.json

🎉 Generated 11 total evidence files
```

### Step 5: Run Demo Pipeline with Dataset Variations

Choose from three specialized dataset variations for testing different compliance scenarios:

#### 🔧 Original Comprehensive Dataset (General Compliance)
```powershell
# Test general compliance detection (COPPA, GDPR, Utah Act)
python demo_pipeline.py original_comprehensive_focused
```
**Features tested:** User registration, content recommendation, crisis intervention  
**Focus:** General compliance with intentional compliance gaps

#### 🔒 Enterprise Security Dataset (Security Vulnerabilities)
```powershell
# Test enterprise security vulnerability detection
python demo_pipeline.py enterprise_security_focused
```
**Features tested:** Threat detection, zero trust architecture, IAM, security monitoring  
**Focus:** Security vulnerabilities and enterprise compliance gaps

#### 🌍 Global Expansion Dataset (International Compliance)
```powershell
# Test international compliance and data sovereignty
python demo_pipeline.py global_expansion_focused
```
**Features tested:** Multi-region compliance, localization, cross-border transfers, content moderation  
**Focus:** International regulations (GDPR, CCPA, PIPEDA, LGPD)

**Expected Output:**
```
� CDS Compliance Detection System - Enhanced Pipeline Demo
================================================================================
🎯 Dataset Variation: Original Comprehensive (or Enterprise Security/Global Expansion)
🎯 Features: Comprehensive artifacts including PRDs, TRDs, design docs, user stories, test cases, and risk assessments
================================================================================

📊 Comprehensive Dataset Loaded:
   📋 Total Features: 3 (varies by dataset: 3-4 features)
   📋 Features with PRDs: 3
   📋 Features with TRDs: 3
   📋 Safety Critical Features: 3
   📋 Age Verification Required: 1
   📋 Parental Consent Required: 1
   ⚖️  Compliance Domains: coppa, gdpr, utah_social_media_act, algorithm_transparency...

🔄 Running enhanced compliance detection pipeline...
Failed to parse Gemini response as JSON...  # Some API rate limiting expected
Google AI Studio analysis failed... # Some failures expected in demo

================================================================================
🎉 Enhanced Pipeline Demo Completed Successfully!

📊 Results Summary:
   • Total Features: 3-4 (varies by dataset)
   • Successfully Processed: 3-4
   • Errors: 0-2 (some expected due to API limits)

📄 Generated Files:
   • Enhanced CSV Results: artifacts\comprehensive_demo_results.csv
   • Comprehensive HTML Report: artifacts\comprehensive_demo_report.html
   • Evidence Files: ./artifacts/evidence/
   • Extended Policy Evidence: ./artifacts/evidence/comprehensive_policy_evidence.json
```

### Step 6: Analyze Results

#### View Comprehensive Results
```powershell
# Open HTML report (Windows)
start artifacts\comprehensive_demo_report.html

# Open HTML report (Mac/Linux)  
open artifacts/comprehensive_demo_report.html

# View CSV results
type artifacts\comprehensive_demo_results.csv
```

#### Check Detected Vulnerabilities
```powershell
# View evidence file with detected issues
type artifacts\evidence\user_registration.json
```

**Example Evidence Output:**
```json
{
  "feature_id": "user_registration",
  "static_analysis": {
    "security_issues": {
      "hardcoded_secrets": 3,        // ✅ Intentionally included
      "sql_injection_risks": 2,      // ✅ Intentionally included  
      "missing_validation": 0,
      "insecure_connections": 0
    }
  },
  "rules_engine": {
    "requires_geo_logic": false,
    "confidence_score": 0.0,         // Low confidence = needs review
    "compliance_domains": ["coppa", "gdpr", "utah_social_media_act"]
  }
}
```

## 📊 Understanding the Demo Output

### CSV Results Structure
```csv
feature_name,compliance_verdict,confidence_score,evidence_count,recommendations
user_registration,REQUIRES_REVIEW,0.85,7,"Implement age verification for Utah compliance"
content_moderation,COMPLIANT,0.92,9,"NCMEC reporting properly configured"
recommendation_engine,NON_COMPLIANT,0.78,5,"Add geographic personalization controls"
```

### HTML Report Contents
The HTML report includes:

- **📋 Executive Summary** - Overall compliance posture
- **🔍 Feature Analysis** - Per-feature compliance decisions
- **⚖️ Regulation Coverage** - Which rules were evaluated
- **📈 Evidence Details** - Static signals and runtime traces
- **💡 Recommendations** - Actionable next steps

### Sample Analysis Results

#### ✅ Compliant Feature Example
```
Feature: content_moderation
Verdict: COMPLIANT (92% confidence)
Evidence: 
  - NCMEC reporting client detected
  - Age-inappropriate content filters active
  - Geographic content policies configured
Recommendation: System properly configured for content compliance
```

#### ⚠️ Needs Review Example
```
Feature: user_registration
Verdict: REQUIRES_REVIEW (85% confidence)  
Evidence:
  - Age collection detected but no verification flow
  - Utah-specific geo-branching missing
  - Parental consent flow not implemented
Recommendation: Implement age verification for Utah Social Media Act compliance
```

## 🎯 What Just Happened?

The demo pipeline executed the complete CDS workflow:

1. **🔍 Static Scanning** - Analyzed 3 sample Python files using semgrep rules
2. **🧪 Runtime Probing** - Mock geographic persona testing (full Playwright integration available)
3. **⚖️ Rules Evaluation** - Applied 7 compliance regulations using JSON Logic
4. **🤖 LLM Analysis** - Generated compliance explanations (using mock Gemini responses)
5. **📊 Report Generation** - Created CSV data and HTML dashboard

## ✅ Validation Checklist

Confirm your demo worked correctly:

- [ ] CLI responded to `cds --help` command
- [ ] `.env` file configured with valid Google AI Studio API key
- [ ] Demo script ran without Python errors
- [ ] CSV file created in `artifacts/demo_results.csv`
- [ ] HTML report generated and viewable
- [ ] Report shows 3 analyzed features with compliance verdicts
- [ ] LLM analysis sections contain actual reasoning (not mock responses)

## 🚀 Next Steps

### For Immediate Use:
1. **[Try with Your Code](../guides/user-manual.md#analyzing-your-repository)** - Run CDS on your actual repository
2. **[Customize Rules](../tutorials/adding-regulations.md)** - Add your organization's compliance requirements
3. **[Configure Integrations](../technical/llm-integration.md)** - Connect real Gemini API for enhanced analysis

### For Production Deployment:
1. **[Installation Guide](../deployment/installation.md)** - Production-ready deployment
2. **[Docker Setup](../deployment/docker-guide.md)** - Containerized deployment
3. **[CI/CD Integration](../deployment/ci-cd.md)** - Automate compliance checking

### For Development:
1. **[Contributing Guide](../development/contributing.md)** - Join the development community
2. **[System Architecture](../architecture/system-overview.md)** - Understand the internals
3. **[Custom Scanners](../tutorials/custom-scanners.md)** - Build new analysis capabilities

## 🛠️ Troubleshooting

### Common Issues

#### ❌ "python: command not found"
**Solution**: Install Python 3.11+ from [python.org](https://python.org/downloads/)

#### ❌ "Permission denied: cannot create venv"
**Solution**: Run PowerShell as Administrator or use:
```powershell
python -m venv venv --system-site-packages
```

#### ❌ "Module 'cds' not found"
**Solution**: Ensure you're in the project directory and virtual environment is activated:
```powershell
cd compliance-detection-system
.\venv\Scripts\Activate.ps1
pip install -e .
```

#### ❌ "GOOGLE_API_KEY not found" or "LLM analysis failed"
**Solution**: Ensure your `.env` file is properly configured:
```powershell
# Check if .env file exists
Get-Content .env

# Should contain:
# GOOGLE_API_KEY=your_actual_api_key_here
# GEMINI_MODEL=gemini-2.0-flash-exp
```

If missing, copy from template and add your API key:
```powershell
copy .env.example .env
notepad .env  # Add your Google AI Studio API key
```

#### ❌ "No output files generated"
**Solution**: Check permissions on the artifacts/ directory:
```powershell
mkdir artifacts -ErrorAction SilentlyContinue
python demo_pipeline.py
```

#### ❌ "Semgrep not found"
This is expected! CDS includes mock implementations for all external tools. For full functionality:
```powershell
pip install semgrep
```

### Getting Help

Still stuck? 

1. **Check [User Manual Troubleshooting](../guides/user-manual.md#troubleshooting)**
2. **Search [GitHub Issues](https://github.com/your-org/compliance-detection-system/issues)**
3. **Create a [Support Request](https://github.com/your-org/compliance-detection-system/issues/new?template=support.md)**

## 🎉 Success!

You've successfully:
- ✅ Installed and configured CDS
- ✅ Executed the complete compliance detection pipeline
- ✅ Generated compliance reports with actionable recommendations
- ✅ Validated the system works end-to-end

**Ready to analyze your own code?** Continue to the **[User Manual](../guides/user-manual.md)** for complete CLI documentation and real-world workflows.

---

**⏱️ Time to Complete**: ~10 minutes  
**📝 Last Updated**: Aug 2025  
**🔄 Next**: [User Manual](../guides/user-manual.md)
