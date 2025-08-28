# User Manual

Complete guide to using the **Compliance Detection System (CDS)** for automated compliance analysis and reporting.

## 📋 Table of Contents

1. [CLI Command Reference](#cli-command-reference)
2. [Understanding CDS Outputs](#understanding-cds-outputs)
3. [Interpreting Compliance Recommendations](#interpreting-compliance-recommendations)
4. [Common Workflows](#common-workflows)
5. [Analyzing Your Repository](#analyzing-your-repository)
6. [Configuration & Customization](#configuration--customization)
7. [Troubleshooting](#troubleshooting)

## 🚀 CLI Command Reference

### Global Options

All CDS commands support these global options:

```powershell
cds [GLOBAL_OPTIONS] COMMAND [ARGS]

Global Options:
  --help          Show help message
  --version       Show CDS version information
  --verbose       Enable detailed logging output
  --config FILE   Path to custom configuration file
```

### Core Commands

#### `cds scan` - Static Analysis

Extract compliance signals from source code using static analysis.

```powershell
cds scan --repo PATH --feature NAME [OPTIONS]
```

**Parameters:**
- `--repo, -r PATH`: Repository path to analyze (required)
- `--feature, -f NAME`: Feature name identifier (required)  
- `--output, -o PATH`: Output evidence file path (optional)

**Example:**
```powershell
# Scan user registration feature
cds scan --repo ./my-app --feature user_registration

# Save evidence to specific file
cds scan -r ./my-app -f user_registration -o evidence/user_reg.json
```

**Output:**
```
🔍 Scanning repository: ./my-app
📋 Feature: user_registration

┌─────────────────┬───────┬──────────────────────────┐
│ Signal Type     │ Count │ Files                    │
├─────────────────┼───────┼──────────────────────────┤
│ Geo Branching   │ 2     │ auth.py, registration.py │
│ Age Checks      │ 1     │ registration.py          │
│ Data Residency  │ 3     │ db.py, storage.py        │
│ Feature Flags   │ 4     │ config.py, flags.py      │
└─────────────────┴───────┴──────────────────────────┘

✅ Evidence saved: artifacts/user_registration_evidence.json
```

#### `cds probe` - Runtime Analysis

Test feature behavior across geographic personas using runtime probes.

```powershell
cds probe --url URL --feature NAME [OPTIONS]
```

**Parameters:**
- `--url, -u URL`: Target application URL (required)
- `--feature, -f NAME`: Feature name to probe (required)
- `--personas PATH`: Custom personas file (optional, defaults to built-in)
- `--timeout SECONDS`: Probe timeout in seconds (default: 30)

**Example:**
```powershell
# Probe user registration from different countries
cds probe --url https://myapp.com --feature user_registration

# Use custom geographic personas
cds probe -u https://myapp.com -f user_registration --personas personas.json
```

**Output:**
```
🧪 Probing feature: user_registration
🌍 Testing 5 geographic personas...

┌──────────────┬─────┬──────────────────┬─────────────────┐
│ Country      │ Age │ Blocked Actions  │ UI States       │
├──────────────┼─────┼──────────────────┼─────────────────┤
│ US (Utah)    │ 16  │ registration     │ age_verify_req  │
│ EU (Germany) │ 14  │ []               │ gdpr_consent    │
│ CA           │ 17  │ []               │ standard_form   │
│ AU           │ 15  │ social_features  │ parental_req    │
│ UK           │ 16  │ []               │ standard_form   │
└──────────────┴─────┴──────────────────┴─────────────────┘

✅ Runtime evidence saved: artifacts/user_registration_runtime.json
```

#### `cds evaluate` - Compliance Rules

Apply compliance rules to collected evidence and generate compliance verdicts.

```powershell
cds evaluate --evidence PATH [OPTIONS]
```

**Parameters:**
- `--evidence, -e PATH`: Evidence file to evaluate (required)
- `--rules PATH`: Custom rules file (optional)
- `--output, -o PATH`: Output evaluation file (optional)

**Example:**
```powershell
# Evaluate collected evidence
cds evaluate --evidence artifacts/user_registration_evidence.json

# Use custom compliance rules
cds evaluate -e evidence.json --rules custom_rules.json
```

**Output:**
```
⚖️ Evaluating compliance rules...
📋 Feature: user_registration

┌─────────────────────────┬─────────────┬────────────────┐
│ Regulation              │ Status      │ Confidence     │
├─────────────────────────┼─────────────┼────────────────┤
│ Utah Social Media Act   │ NON_COMPLIANT │ 0.92          │
│ COPPA                   │ COMPLIANT    │ 0.88          │
│ GDPR Article 8          │ REQUIRES_REVIEW │ 0.75       │
│ NCMEC Reporting         │ NOT_APPLICABLE │ 1.00        │
│ EU DSA                  │ COMPLIANT    │ 0.85          │
│ CA Privacy Act          │ COMPLIANT    │ 0.79          │
│ AU Privacy Act          │ REQUIRES_REVIEW │ 0.68       │
└─────────────────────────┴─────────────┴────────────────┘

🎯 Overall Verdict: REQUIRES_REVIEW (0.82 confidence)
✅ Evaluation saved: artifacts/user_registration_evaluation.json
```

#### `cds explain` - LLM Analysis

Generate AI-powered compliance explanations and recommendations using LLM reasoning.

```powershell
cds explain --evaluation PATH [OPTIONS]
```

**Parameters:**
- `--evaluation, -e PATH`: Evaluation results to explain (required)
- `--model NAME`: LLM model to use (default: gemini-1.5-pro)
- `--output, -o PATH`: Output explanation file (optional)

**Example:**
```powershell
# Generate explanations for evaluation results
cds explain --evaluation artifacts/user_registration_evaluation.json

# Use specific LLM model
cds explain -e evaluation.json --model gemini-1.5-pro-latest
```

**Output:**
```
🤖 Generating LLM explanations...
📋 Feature: user_registration

🔍 Analysis Summary:
The user registration feature shows mixed compliance across jurisdictions. Key concerns:

⚠️ Utah Social Media Act - NON_COMPLIANT
• Age collection detected but no verification mechanism
• Missing parental consent workflow for minors
• Social features accessible without age gate

✅ COPPA - COMPLIANT  
• Proper age collection and data handling
• Privacy policy includes children's data protection

⚠️ GDPR Article 8 - REQUIRES_REVIEW
• Age verification present but mechanism unclear
• Consent flow may need parental approval enhancement

💡 Recommendations:
1. Implement robust age verification (document upload, credit card, etc.)
2. Add parental consent workflow for users under 18 in Utah
3. Create jurisdiction-specific registration flows
4. Audit social feature access controls

✅ Explanation saved: artifacts/user_registration_explanation.json
```

#### `cds pipeline` - End-to-End Analysis

Execute the complete compliance detection pipeline from scanning to reporting.

```powershell
cds pipeline --repo PATH --features LIST [OPTIONS]
```

**Parameters:**
- `--repo, -r PATH`: Repository to analyze (required)
- `--features, -f LIST`: Comma-separated feature names (required)
- `--output-dir, -o PATH`: Output directory (default: artifacts/)
- `--format FORMAT`: Output format csv,html,json (default: csv,html)
- `--probe-url URL`: URL for runtime probing (optional)

**Example:**
```powershell
# Analyze multiple features end-to-end
cds pipeline --repo ./my-app --features user_registration,content_moderation,recommendation_engine

# Include runtime probing and custom output
cds pipeline -r ./my-app -f user_registration,payments --probe-url https://staging.myapp.com -o compliance_reports/
```

**Output:**
```
🔄 Starting CDS Pipeline...

🔍 Phase 1: Static Analysis
✅ user_registration - 7 signals extracted
✅ content_moderation - 12 signals extracted  
✅ recommendation_engine - 5 signals extracted

🧪 Phase 2: Runtime Probes (Optional)
✅ user_registration - 5 personas tested
✅ content_moderation - 5 personas tested
✅ recommendation_engine - 5 personas tested

⚖️ Phase 3: Compliance Evaluation
✅ 21 compliance rules applied across 3 features
✅ Overall compliance score: 0.84

🤖 Phase 4: LLM Analysis  
✅ Generated explanations for 3 features
✅ Identified 8 actionable recommendations

📊 Phase 5: Report Generation
✅ CSV exported: artifacts/pipeline_results.csv
✅ HTML report: artifacts/pipeline_report.html
✅ JSON data: artifacts/pipeline_data.json

🎉 Pipeline completed in 45 seconds
```

#### `cds version` - System Information

Display version information and system diagnostics.

```powershell
cds version [OPTIONS]
```

**Options:**
- `--diagnostics`: Show detailed system information
- `--dependencies`: List installed dependencies and versions

**Example:**
```powershell
cds version --diagnostics
```

**Output:**
```
🔧 CDS Version Information

Version: 1.0.0
Build: 2024.12.15
Python: 3.11.7
Platform: Windows-10-10.0.22631-SP0

📦 Core Dependencies:
✅ typer 0.9.0
✅ rich 13.7.0  
✅ pydantic 2.5.2
✅ pandas 2.1.4
✅ jinja2 3.1.2

🔍 Scanner Dependencies:
⚠️ semgrep - not installed (using mock implementation)
✅ tree-sitter 0.20.4

🧪 Runtime Dependencies:
⚠️ playwright - not installed (using mock implementation)

🤖 LLM Dependencies:
⚠️ google-cloud-aiplatform - not configured
✅ httpx 0.25.2 (for API requests)

💡 Run 'pip install semgrep playwright google-cloud-aiplatform' for full functionality
```

## 📊 Understanding CDS Outputs

### Evidence Structure

CDS collects evidence in a structured **Evidence Pack** format:

```json
{
  "feature_name": "user_registration",
  "repo": "./my-app", 
  "timestamp": "2024-12-15T10:30:00Z",
  "static_signals": {
    "geo_branching": [
      {
        "file": "auth.py",
        "line": 45,
        "countries": ["US", "EU", "CA"],
        "message": "Geographic branching detected in user registration flow"
      }
    ],
    "age_checks": [
      {
        "file": "registration.py", 
        "line": 123,
        "lib": "dateutil",
        "method": "parse_birthdate",
        "message": "Age calculation from birthdate"
      }
    ],
    "data_residency": [
      {
        "file": "storage.py",
        "line": 67, 
        "region": "EU",
        "service": "user_data_store",
        "message": "EU data residency configuration"
      }
    ]
  },
  "runtime_signals": {
    "persona": {"country": "US", "age": 16},
    "blocked_actions": ["social_connect", "friend_invite"],
    "ui_states": ["age_verification_required"],
    "flag_resolutions": [
      {"name": "utah_compliance", "value": true}
    ]
  }
}
```

### Compliance Evaluation Results

Rules evaluation produces structured compliance verdicts:

```json
{
  "feature_name": "user_registration",
  "overall_verdict": "REQUIRES_REVIEW",
  "confidence_score": 0.82,
  "rule_results": [
    {
      "rule_name": "Utah Social Media Act",
      "regulation_id": "utah_social_media_2024",
      "verdict": "NON_COMPLIANT", 
      "confidence": 0.92,
      "reasoning": "Age verification required but not implemented",
      "evidence_refs": ["static.age_checks", "runtime.blocked_actions"]
    }
  ],
  "recommendations": [
    {
      "priority": "HIGH",
      "action": "Implement age verification flow",
      "regulation": "Utah Social Media Act",
      "effort": "2-3 weeks development"
    }
  ]
}
```

### Final Record Format

The complete analysis combines all evidence and reasoning:

```json
{
  "feature_name": "user_registration",
  "analysis_timestamp": "2024-12-15T10:35:00Z",
  "compliance_decision": {
    "overall_verdict": "REQUIRES_REVIEW",
    "confidence_score": 0.82,
    "risk_level": "MEDIUM"
  },
  "evidence_summary": {
    "static_signals_count": 7,
    "runtime_signals_count": 5,
    "total_evidence_items": 12
  },
  "llm_analysis": {
    "model": "gemini-1.5-pro",
    "explanation": "The registration feature demonstrates partial compliance...",
    "key_risks": ["Utah age verification gap", "GDPR consent clarity"],
    "recommendations": [
      "Implement document-based age verification",
      "Add parental consent workflow",
      "Create jurisdiction-specific flows"
    ]
  }
}
```

## 📈 Interpreting Compliance Recommendations  

### Verdict Classifications

| Verdict | Meaning | Action Required |
|---------|---------|-----------------|
| **COMPLIANT** | Feature meets compliance requirements | ✅ No immediate action; continue monitoring |
| **NON_COMPLIANT** | Clear compliance violations detected | 🚨 **Immediate remediation required** |
| **REQUIRES_REVIEW** | Potential issues or insufficient evidence | ⚠️ **Manual review and possible fixes** |
| **NOT_APPLICABLE** | Regulation doesn't apply to this feature | ℹ️ No action needed |

### Confidence Score Interpretation

| Score Range | Interpretation | Action |
|-------------|----------------|--------|
| **0.90 - 1.00** | High confidence in verdict | Trust the analysis, act on recommendations |
| **0.75 - 0.89** | Good confidence | Review evidence, likely actionable |
| **0.60 - 0.74** | Moderate confidence | Manual validation recommended |
| **0.00 - 0.59** | Low confidence | Requires human expert review |

### Risk Level Guidelines

| Risk Level | Characteristics | Response Time |
|------------|----------------|---------------|
| **CRITICAL** | Legal compliance violations, user safety risks | **Immediate (24-48 hours)** |
| **HIGH** | Regulatory non-compliance, audit findings | **Urgent (1-2 weeks)** |
| **MEDIUM** | Best practice deviations, process improvements | **Planned (1-2 sprints)** |
| **LOW** | Documentation gaps, monitoring enhancements | **Backlog (next quarter)** |

## 🔄 Common Workflows

### Workflow 1: New Feature Compliance Check

**Scenario**: Validate compliance before deploying a new feature

```powershell
# 1. Scan the feature for compliance signals
cds scan --repo . --feature new_messaging_system

# 2. Test runtime behavior (if testable)  
cds probe --url https://staging.myapp.com --feature messaging

# 3. Evaluate against compliance rules
cds evaluate --evidence artifacts/new_messaging_system_evidence.json

# 4. Generate actionable recommendations
cds explain --evaluation artifacts/new_messaging_system_evaluation.json

# 5. Review HTML report for team discussion
start artifacts/new_messaging_system_explanation.html
```

### Workflow 2: Batch Repository Analysis

**Scenario**: Audit compliance across all features in your codebase

```powershell
# Run complete pipeline on all major features
cds pipeline --repo . --features user_auth,content_upload,recommendation_engine,payment_flow,social_features

# Review the comprehensive HTML dashboard
start artifacts/pipeline_report.html

# Export results for compliance team
copy artifacts/pipeline_results.csv "compliance_audit_$(Get-Date -Format 'yyyy-MM-dd').csv"
```

### Workflow 3: Regulatory Update Response

**Scenario**: New regulation passed, need to assess impact

```powershell
# 1. Add new regulation rules (see tutorials/adding-regulations.md)
# 2. Re-evaluate all features with updated rules
cds pipeline --repo . --features user_auth,content_moderation,data_collection --rules regulations/2024_updates.json

# 3. Generate impact report
cds explain --evaluation artifacts/pipeline_evaluation.json --output compliance/regulatory_impact_2024.json

# 4. Prioritize remediation efforts based on risk scores
```

### Workflow 4: CI/CD Integration

**Scenario**: Automate compliance checking in your deployment pipeline

```yaml
# .github/workflows/compliance-check.yml
name: Compliance Check
on: [pull_request]

jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install CDS
      run: pip install compliance-detection-system
      
    - name: Run Compliance Analysis
      run: |
        cds pipeline --repo . --features user_registration,content_upload
        
    - name: Upload Results
      uses: actions/upload-artifact@v3
      with:
        name: compliance-reports
        path: artifacts/
```

## 🔧 Analyzing Your Repository

### Preparing Your Repository

**1. Identify Features for Analysis**

Create a feature mapping document:
```yaml
# compliance_features.yml
features:
  user_registration:
    paths: ["auth/", "registration/", "users/"]
    description: "User account creation and profile setup"
    compliance_areas: ["age_verification", "data_collection", "geo_compliance"]
    
  content_moderation:  
    paths: ["moderation/", "content/", "safety/"]
    description: "User-generated content review and safety"
    compliance_areas: ["ncmec_reporting", "harmful_content", "age_appropriate"]
    
  recommendation_engine:
    paths: ["recommendations/", "ml/", "personalization/"] 
    description: "Personalized content and user recommendations"
    compliance_areas: ["algorithmic_transparency", "filter_bubbles", "age_appropriate"]
```

**2. Configure Repository Structure**

CDS works best with clear directory structures:
```
my-app/
├── src/                    # Source code to analyze
│   ├── auth/              # Authentication features
│   ├── content/           # Content management 
│   └── recommendations/   # ML/recommendation features
├── config/                # Configuration files
├── tests/                 # Test files (analyzed for compliance test coverage)
└── compliance/            # CDS configuration and custom rules
    ├── features.yml       # Feature definitions
    ├── custom_rules.json  # Organization-specific rules
    └── personas.json      # Custom geographic test personas
```

**3. Create Feature-Specific Configuration**

```json
// compliance/custom_rules.json
{
  "organization": "MyCompany",
  "rules": [
    {
      "name": "Internal Privacy Policy",
      "description": "MyCompany data handling requirements",
      "logic": {
        "if": [
          {"var": "static.data_collection"},
          "REQUIRES_REVIEW",
          "COMPLIANT"
        ]
      },
      "confidence": 0.8
    }
  ]
}
```

### Running Analysis on Your Code

**Step 1: Start with Single Feature**

```powershell
# Test CDS on one well-defined feature first
cds scan --repo . --feature user_registration --output evidence/user_registration.json

# Review the extracted evidence
Get-Content evidence/user_registration.json | ConvertFrom-Json | Format-List
```

**Step 2: Validate Evidence Quality**

Check that CDS is finding relevant signals:
- **Geo-branching patterns**: Country/region-based logic
- **Age verification**: Birthdate collection, age calculations
- **Data residency**: Geographic data storage decisions
- **Feature flags**: Compliance-related toggles
- **Reporting clients**: NCMEC, law enforcement integrations

**Step 3: Expand to Multiple Features**

```powershell
# Run pipeline on core features
cds pipeline --repo . --features user_registration,content_upload,recommendations

# Review HTML report for insights
start artifacts/pipeline_report.html
```

**Step 4: Customize for Your Domain**

- Add domain-specific semgrep rules in `data/rules/custom/`
- Define organization compliance rules in `compliance/rules.json`
- Create realistic test personas in `compliance/personas.json`

## ⚙️ Configuration & Customization

### Environment Variables

Configure CDS behavior via environment variables:

```powershell
# Core Configuration
$env:CDS_LOG_LEVEL = "INFO"                    # DEBUG, INFO, WARNING, ERROR
$env:CDS_OUTPUT_DIR = "compliance_reports"     # Default output directory
$env:CDS_CONFIG_FILE = "cds_config.yml"       # Configuration file path

# LLM Integration
$env:GOOGLE_CLOUD_PROJECT = "my-project-id"   # GCP Project for Vertex AI
$env:GOOGLE_CLOUD_REGION = "us-central1"      # GCP Region
$env:CDS_LLM_MODEL = "gemini-1.5-pro"         # LLM model selection
$env:CDS_LLM_MAX_TOKENS = "4096"              # Max response tokens

# Scanner Configuration  
$env:CDS_SEMGREP_TIMEOUT = "300"              # Semgrep timeout in seconds
$env:CDS_SCANNER_THREADS = "4"                # Parallel scanning threads

# Runtime Probes
$env:CDS_PLAYWRIGHT_TIMEOUT = "30000"         # Playwright timeout in ms
$env:CDS_PROBE_RETRIES = "3"                  # Retry failed probes

# Database
$env:CDS_DATABASE_URL = "sqlite:///cds.db"    # SQLite database path
```

### Configuration File

Create `cds_config.yml` for persistent settings:

```yaml
# cds_config.yml
logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  
output:
  directory: "artifacts"
  formats: ["csv", "html", "json"]
  
scanner:
  timeout: 300
  parallel_jobs: 4
  custom_rules_dir: "compliance/rules"
  
runtime:
  default_personas: "compliance/personas.json"
  timeout: 30
  retry_attempts: 3
  
llm:
  provider: "gemini"
  model: "gemini-1.5-pro"
  max_tokens: 4096
  temperature: 0.1
  
database:
  url: "sqlite:///evidence.db"
  backup_enabled: true
  retention_days: 90
```

### Custom Semgrep Rules

Add organization-specific rules in `data/rules/custom/`:

```yaml
# data/rules/custom/mycompany_privacy.yml
rules:
  - id: mycompany-data-collection  
    message: MyCompany data collection detected
    languages: [python]
    severity: INFO
    pattern-either:
      - pattern: collect_user_data($...ARGS)
      - pattern: track_user_behavior($...ARGS)
      - pattern: analytics.track($USER, $EVENT)
    metadata:
      category: data_collection
      compliance_area: privacy
      
  - id: mycompany-age-verification
    message: Age verification flow detected
    languages: [python]
    severity: INFO
    patterns:
      - pattern: verify_age($AGE)
      - pattern: age_gate_required()
      - pattern: parental_consent_flow()
    metadata:
      category: age_verification
      compliance_area: child_safety
```

### Custom JSON Logic Rules

Define compliance logic in `compliance/rules.json`:

```json
{
  "rules": [
    {
      "name": "MyCompany Child Safety",
      "description": "Internal child safety requirements",
      "regulation_id": "mycompany_child_safety_v1",
      "logic": {
        "if": [
          {"and": [
            {">=": [{"var": "static.age_checks.length"}, 1]},
            {">=": [{"var": "static.geo_branching.length"}, 1]}
          ]},
          "COMPLIANT",
          {
            "if": [
              {">=": [{"var": "static.age_checks.length"}, 1]},
              "REQUIRES_REVIEW", 
              "NON_COMPLIANT"
            ]
          }
        ]
      },
      "confidence": 0.85,
      "priority": "HIGH"
    }
  ]
}
```

## 🛠️ Troubleshooting

### Installation Issues

#### ❌ "Python version not supported"
```powershell
# Check Python version
python --version

# If < 3.11, install newer Python from python.org
# Or use pyenv/conda to manage versions
conda create -n cds python=3.11
conda activate cds
```

#### ❌ "Package installation failed"
```powershell
# Upgrade pip and try again
python -m pip install --upgrade pip setuptools wheel
pip install -e .

# Or use UV for faster installs
pip install uv
uv pip install -e .
```

#### ❌ "Virtual environment activation failed"
```powershell
# PowerShell execution policy issue
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate again
.\venv\Scripts\Activate.ps1
```

### Scanning Issues

#### ❌ "No static signals found"

**Possible Causes:**
1. **Wrong file types**: CDS primarily scans Python files
2. **No matching patterns**: Your code doesn't match semgrep rules
3. **Path issues**: Repository path is incorrect

**Solutions:**
```powershell
# Check repository structure
Get-ChildItem -Recurse -Include "*.py" | Measure-Object

# Run with verbose logging
$env:CDS_LOG_LEVEL = "DEBUG"
cds scan --repo . --feature test_feature

# Test specific file patterns
cds scan --repo ./src --feature test_feature
```

#### ❌ "Semgrep command failed" 

```powershell
# Install semgrep for full functionality
pip install semgrep

# Or verify mock mode is working
cds version --diagnostics
```

#### ❌ "Tree-sitter parsing errors"

```powershell
# Install language parsers
pip install tree-sitter-languages

# Check file encoding issues
file *.py  # Should show UTF-8 encoding
```

### Runtime Probe Issues

#### ❌ "Playwright browser failed"

```powershell
# Install Playwright browsers
pip install playwright
playwright install chromium

# Or use mock probes for development
$env:CDS_RUNTIME_MOCK = "true"
cds probe --url https://example.com --feature test
```

#### ❌ "Target URL not accessible"

**Solutions:**
1. **VPN/Network**: Ensure target URL is accessible
2. **Authentication**: Add authentication tokens if needed  
3. **Local development**: Use localhost URLs for local testing

```powershell
# Test URL accessibility
curl -I https://your-app.com

# Use local development server
cds probe --url http://localhost:3000 --feature test
```

### LLM Integration Issues

#### ❌ "Google Cloud authentication failed"

```powershell
# Set up ADC (Application Default Credentials)
gcloud auth application-default login

# Or use service account key
$env:GOOGLE_APPLICATION_CREDENTIALS = "path/to/service-account.json"

# Verify GCP project configuration  
gcloud config get-value project
```

#### ❌ "Vertex AI API not enabled"

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to APIs & Services > Library
3. Search for "Vertex AI API" 
4. Click Enable

#### ❌ "LLM request timeout/rate limits"

```powershell
# Reduce request frequency
$env:CDS_LLM_RATE_LIMIT = "10"  # Requests per minute

# Use smaller analysis batches
cds explain --evaluation results.json --batch-size 5

# Enable request caching
$env:CDS_LLM_CACHE = "true"
```

### Output Generation Issues

#### ❌ "No HTML report generated"

```powershell
# Check output directory permissions
Test-Path artifacts -PathType Container
New-Item -ItemType Directory -Path artifacts -Force

# Verify template files
Get-ChildItem cds/templates/ -Include "*.html"

# Test with specific output path
cds pipeline --repo . --features test --output-dir ./reports/
```

#### ❌ "CSV export empty/malformed"

**Common Issues:**
1. **No evidence collected**: Check scanning phase
2. **Unicode encoding**: Use UTF-8 compatible CSV viewers  
3. **Path separators**: Use forward slashes in file paths

```powershell
# Check evidence was collected
Get-Content artifacts/evidence_pack.json | ConvertFrom-Json | Select-Object -ExpandProperty static_signals

# Test CSV with PowerShell
Import-Csv artifacts/results.csv | Format-Table
```

### Performance Issues

#### ❌ "Scanning very slow on large repositories"

```powershell
# Increase parallel jobs
$env:CDS_SCANNER_THREADS = "8"

# Exclude irrelevant directories
cds scan --repo . --feature test --exclude "node_modules,*.git,build,dist"

# Use incremental scanning
cds scan --repo . --feature test --since "last-scan"
```

#### ❌ "Out of memory during analysis"

```powershell
# Process features individually
cds scan --repo . --feature feature1
cds scan --repo . --feature feature2

# Reduce concurrent operations
$env:CDS_MAX_CONCURRENT = "2"

# Enable streaming mode for large outputs
$env:CDS_STREAMING = "true"
```

### Configuration Issues

#### ❌ "Environment variables not recognized"

```powershell
# List all CDS environment variables
Get-ChildItem Env: | Where-Object Name -like "CDS_*"

# Set in PowerShell profile for persistence
Add-Content $PROFILE "`$env:CDS_LOG_LEVEL = 'INFO'"
```

#### ❌ "Configuration file not found"

```powershell
# Check default locations
Test-Path cds_config.yml
Test-Path ~/.cds/config.yml
Test-Path $env:CDS_CONFIG_FILE

# Create minimal config
@"
logging:
  level: INFO
output:
  directory: artifacts
"@ | Out-File -FilePath cds_config.yml
```

### Getting Additional Help

#### 🔍 Enable Debug Logging

```powershell
$env:CDS_LOG_LEVEL = "DEBUG"
cds scan --repo . --feature test_feature 2>&1 | Tee-Object debug.log
```

#### 📊 Generate Diagnostic Report

```powershell
cds version --diagnostics > system_info.txt
Get-Content system_info.txt
```

#### 🤝 Community Support Channels

1. **GitHub Issues**: [Create issue](https://github.com/your-org/compliance-detection-system/issues/new)
2. **Slack**: #compliance-detection-system  
3. **Stack Overflow**: Tag questions with `compliance-detection-system`
4. **Documentation**: [Report doc issues](https://github.com/your-org/compliance-detection-system/issues/new?template=documentation.md)

#### 📋 Issue Report Template

When reporting issues, include:

```powershell
# System information
cds version --diagnostics

# Command that failed
cds scan --repo . --feature test_feature

# Error output (with debug logging)
$env:CDS_LOG_LEVEL = "DEBUG"
cds scan --repo . --feature test_feature

# Repository structure (if relevant) 
Get-ChildItem -Recurse -Include "*.py" | Select-Object FullName
```

---

**📝 Last Updated**: December 2024  
**🔄 Next Steps**: [System Architecture](../architecture/system-overview.md) | [Adding Regulations Tutorial](../tutorials/adding-regulations.md)  
**⏱️ Reading Time**: ~45 minutes
