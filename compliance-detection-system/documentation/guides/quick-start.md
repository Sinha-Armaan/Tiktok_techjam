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

- [ ] **Virtual environment** support (built into Python 3.11+)
- [ ] **Internet connection** for package downloads

### Optional (for full functionality):
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

### Step 2: Verify Installation

```powershell
# Test CLI is working
cds --help

# Expected output:
# Usage: cds [OPTIONS] COMMAND [ARGS]...
# 
# Compliance Detection System - Detect geo-specific compliance requirements
```

### Step 3: Run Demo Pipeline

```powershell
# Execute the complete demo pipeline
python demo_pipeline.py
```

**Expected Output:**
```
🔄 Starting CDS Demo Pipeline...

🔍 Scanning 3 sample features...
✅ user_registration - 4 static signals extracted
✅ content_moderation - 6 static signals extracted  
✅ recommendation_engine - 3 static signals extracted

⚖️ Evaluating compliance rules...
✅ 3 features evaluated against 7 compliance regulations

🤖 Generating LLM explanations...
✅ Compliance reasoning generated for all features

📊 Exporting results...
✅ CSV exported: artifacts/demo_results.csv
✅ HTML report: artifacts/demo_report.html

🎉 Demo completed successfully!
```

### Step 4: View Results

Open the generated HTML report in your browser:

```powershell
# Windows
start artifacts\demo_report.html

# Or view the raw data
type artifacts\demo_results.csv | Select-Object -First 10
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
- [ ] Demo script ran without Python errors
- [ ] CSV file created in `artifacts/demo_results.csv`
- [ ] HTML report generated and viewable
- [ ] Report shows 3 analyzed features with compliance verdicts

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
**📝 Last Updated**: December 2024  
**🔄 Next**: [User Manual](../guides/user-manual.md)
