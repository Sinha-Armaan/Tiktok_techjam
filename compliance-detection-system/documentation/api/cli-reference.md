# CLI Command Reference

Complete command-line interface reference for the **Compliance Detection System (CDS)**. All commands, options, and usage examples.

## 📋 Table of Contents

1. [Global Options](#global-options)
2. [Command Overview](#command-overview)
3. [Individual Commands](#individual-commands)
   - [cds scan](#cds-scan---static-analysis)
   - [cds probe](#cds-probe---runtime-analysis)
   - [cds evaluate](#cds-evaluate---compliance-rules)
   - [cds explain](#cds-explain---llm-analysis)
   - [cds pipeline](#cds-pipeline---end-to-end-analysis)
   - [cds version](#cds-version---system-information)
4. [Input/Output Formats](#inputoutput-formats)
5. [Exit Codes](#exit-codes)
6. [Environment Variables](#environment-variables)
7. [Configuration Files](#configuration-files)

## 🌐 Global Options

All CDS commands support these global options:

```powershell
cds [GLOBAL_OPTIONS] COMMAND [ARGS]
```

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--help` | `-h` | Show help message | N/A |
| `--version` | `-v` | Show CDS version | N/A |
| `--verbose` | N/A | Enable detailed logging | `INFO` |
| `--config FILE` | N/A | Path to configuration file | `cds_config.yml` |
| `--output-dir DIR` | `-o` | Base output directory | `artifacts/` |
| `--no-color` | N/A | Disable colored output | Colored |

### Global Option Examples

```powershell
# Show version information
cds --version

# Run with verbose logging
cds --verbose scan --repo . --feature user_auth

# Use custom configuration
cds --config my_config.yml pipeline --repo . --features user_auth
```

## 📊 Command Overview

| Command | Purpose | Time | Output |
|---------|---------|------|---------|
| `scan` | Extract static signals from code | ~5-30s | Evidence JSON |
| `probe` | Test runtime behavior across personas | ~30-60s | Runtime JSON |
| `evaluate` | Apply compliance rules to evidence | ~2-5s | Rules JSON |
| `explain` | Generate LLM explanations | ~5-15s | Explanation JSON |
| `pipeline` | Complete end-to-end analysis | ~45-90s | CSV, HTML, JSON |
| `version` | System information and diagnostics | ~1s | Version info |

## 🔍 Individual Commands

### `cds scan` - Static Analysis

Extract compliance signals from source code using static analysis tools (semgrep, tree-sitter).

#### Syntax

```powershell
cds scan --repo PATH --feature NAME [OPTIONS]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--repo, -r` | Path | ✅ | Repository path to analyze |
| `--feature, -f` | String | ✅ | Feature name identifier |
| `--output, -o` | Path | ❌ | Output evidence file path |
| `--rules-dir` | Path | ❌ | Custom semgrep rules directory |
| `--exclude` | String | ❌ | Comma-separated exclude patterns |
| `--include` | String | ❌ | Comma-separated include patterns |
| `--timeout` | Integer | ❌ | Scanner timeout in seconds |
| `--parallel-jobs` | Integer | ❌ | Number of parallel scanner jobs |

#### Examples

**Basic Usage:**
```powershell
# Scan user registration feature
cds scan --repo ./my-app --feature user_registration
```

**Advanced Usage:**
```powershell
# Custom output location with exclusions
cds scan -r ./my-app -f user_registration -o evidence/user_reg.json --exclude "node_modules,*.git"

# Custom rules with increased timeout
cds scan --repo ./my-app --feature payment_flow --rules-dir ./custom_rules --timeout 600
```

#### Output Format

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
        "message": "Geographic branching detected"
      }
    ],
    "age_checks": [
      {
        "file": "registration.py", 
        "line": 123,
        "lib": "dateutil",
        "method": "parse_birthdate"
      }
    ],
    "data_residency": [],
    "reporting_clients": ["ncmec_client"],
    "reco_system": true,
    "pf_controls": false,
    "flags": [
      {"name": "age_verification_enabled", "file": "config.py", "line": 67}
    ],
    "tags": ["authentication", "user_data", "age_sensitive"]
  }
}
```

#### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success - signals extracted |
| `1` | Error - invalid repository path |
| `2` | Error - scanner failure |
| `3` | Warning - partial results |

---

### `cds probe` - Runtime Analysis

Test application behavior across different geographic personas using browser automation.

#### Syntax

```powershell
cds probe --url URL --feature NAME [OPTIONS]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--url, -u` | URL | ✅ | Target application URL |
| `--feature, -f` | String | ✅ | Feature name to probe |
| `--personas` | Path | ❌ | Custom personas file |
| `--timeout` | Integer | ❌ | Probe timeout in seconds (default: 30) |
| `--browser` | String | ❌ | Browser type: chromium, firefox, webkit |
| `--headless` | Boolean | ❌ | Run browser in headless mode |
| `--viewport` | String | ❌ | Browser viewport size (e.g., "1920x1080") |
| `--user-agent` | String | ❌ | Custom user agent string |
| `--auth-token` | String | ❌ | Authentication token for protected endpoints |

#### Examples

**Basic Usage:**
```powershell
# Probe user registration across default personas
cds probe --url https://myapp.com --feature user_registration
```

**Advanced Usage:**
```powershell
# Custom personas with authentication
cds probe -u https://staging.myapp.com -f messaging --personas ./custom_personas.json --auth-token "$env:AUTH_TOKEN"

# Desktop viewport with extended timeout
cds probe --url https://myapp.com --feature video_upload --viewport "1920x1080" --timeout 60
```

#### Personas Format

```json
{
  "personas": [
    {
      "id": "us_utah_minor",
      "country": "US",
      "state": "Utah",
      "age": 16,
      "language": "en-US",
      "timezone": "America/Denver",
      "test_scenarios": ["registration", "social_features"],
      "geo_location": {
        "latitude": 39.3210,
        "longitude": -111.0937
      }
    },
    {
      "id": "eu_germany_adult", 
      "country": "DE",
      "age": 25,
      "language": "de-DE",
      "timezone": "Europe/Berlin",
      "gdpr_mode": true,
      "test_scenarios": ["data_collection", "consent_flows"]
    }
  ]
}
```

#### Output Format

```json
{
  "feature_name": "user_registration",
  "url": "https://myapp.com",
  "timestamp": "2024-12-15T10:35:00Z",
  "runtime_signals": {
    "personas_tested": [
      {
        "persona": {"country": "US", "age": 16},
        "blocked_actions": ["social_connect", "friend_invite"],
        "ui_states": ["age_verification_required", "parental_consent_modal"],
        "flag_resolutions": [
          {"name": "utah_compliance", "value": true}
        ],
        "network": [
          {"host": "api.myapp.com", "method": "POST", "path": "/user/register"}
        ]
      }
    ],
    "summary": {
      "total_personas": 5,
      "successful_probes": 5,
      "failed_probes": 0,
      "unique_behaviors": 3
    }
  }
}
```

---

### `cds evaluate` - Compliance Rules

Apply compliance rules to collected evidence and generate compliance verdicts.

#### Syntax

```powershell
cds evaluate --evidence PATH [OPTIONS]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--evidence, -e` | Path | ✅ | Evidence file to evaluate |
| `--rules` | Path | ❌ | Custom rules file |
| `--output, -o` | Path | ❌ | Output evaluation file |
| `--regulations` | String | ❌ | Comma-separated regulation IDs to apply |
| `--confidence-threshold` | Float | ❌ | Minimum confidence threshold (0.0-1.0) |
| `--include-explanations` | Boolean | ❌ | Include detailed rule explanations |

#### Examples

**Basic Usage:**
```powershell
# Evaluate evidence against all rules
cds evaluate --evidence artifacts/user_registration_evidence.json
```

**Advanced Usage:**
```powershell
# Specific regulations with custom confidence threshold
cds evaluate -e evidence.json --regulations "utah_social_media,coppa,gdpr_article8" --confidence-threshold 0.8

# Custom rules with detailed explanations
cds evaluate --evidence evidence.json --rules custom_rules.json --include-explanations
```

#### Rules Configuration Format

```json
{
  "rules": [
    {
      "name": "Utah Social Media Act - Age Verification",
      "regulation_id": "utah_social_media_2024",
      "description": "Utah requires age verification for social media features",
      "jurisdiction": "US-UT",
      "logic": {
        "if": [
          {"and": [
            {">=": [{"var": "static.geo_branching.length"}, 1]},
            {"in": ["US", {"var": "static.geo_branching.0.countries"}]},
            {">=": [{"var": "static.age_checks.length"}, 1]}
          ]},
          "COMPLIANT",
          "NON_COMPLIANT"
        ]
      },
      "confidence_factors": {
        "geo_specificity": 0.3,
        "age_verification": 0.4,
        "implementation_quality": 0.3
      },
      "priority": "HIGH"
    }
  ]
}
```

#### Output Format

```json
{
  "feature_name": "user_registration",
  "evaluation_timestamp": "2024-12-15T10:40:00Z",
  "overall_verdict": "REQUIRES_REVIEW",
  "confidence_score": 0.82,
  "risk_level": "MEDIUM",
  "rule_results": [
    {
      "rule_name": "Utah Social Media Act",
      "regulation_id": "utah_social_media_2024",
      "verdict": "NON_COMPLIANT",
      "confidence": 0.92,
      "reasoning": "Age verification required but not implemented",
      "evidence_refs": ["static.age_checks", "runtime.blocked_actions"],
      "priority": "HIGH"
    }
  ],
  "recommendations": [
    {
      "priority": "HIGH",
      "action": "Implement age verification flow",
      "regulation": "Utah Social Media Act",
      "effort_estimate": "2-3 weeks",
      "evidence_gap": "No age verification mechanism detected"
    }
  ]
}
```

---

### `cds explain` - LLM Analysis

Generate AI-powered compliance explanations and actionable recommendations.

#### Syntax

```powershell
cds explain --evaluation PATH [OPTIONS]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--evaluation, -e` | Path | ✅ | Evaluation results to explain |
| `--model` | String | ❌ | LLM model to use |
| `--temperature` | Float | ❌ | LLM temperature (0.0-1.0) |
| `--max-tokens` | Integer | ❌ | Maximum response tokens |
| `--output, -o` | Path | ❌ | Output explanation file |
| `--include-policy-context` | Boolean | ❌ | Include regulatory text snippets |
| `--explanation-style` | String | ❌ | Style: technical, executive, legal |

#### Examples

**Basic Usage:**
```powershell
# Generate explanations with default settings
cds explain --evaluation artifacts/user_registration_evaluation.json
```

**Advanced Usage:**
```powershell
# Executive-style explanations with policy context
cds explain -e evaluation.json --explanation-style executive --include-policy-context --max-tokens 2048

# Technical deep-dive with specific model
cds explain --evaluation evaluation.json --model gemini-1.5-pro-latest --explanation-style technical --temperature 0.1
```

#### Model Options

| Model | Description | Use Case |
|-------|-------------|----------|
| `gemini-1.5-pro` | Default balanced model | General compliance analysis |
| `gemini-1.5-pro-latest` | Latest version with improvements | Enhanced reasoning |
| `gemini-1.0-pro` | Faster, less detailed model | Quick explanations |

#### Output Format

```json
{
  "feature_name": "user_registration",
  "analysis_timestamp": "2024-12-15T10:45:00Z",
  "model_used": "gemini-1.5-pro",
  "llm_analysis": {
    "executive_summary": "The user registration feature shows mixed compliance across jurisdictions with critical gaps in Utah-specific age verification requirements.",
    "detailed_analysis": {
      "compliant_areas": [
        {
          "regulation": "COPPA",
          "reasoning": "Proper age collection and data handling procedures are implemented with appropriate privacy policy coverage."
        }
      ],
      "non_compliant_areas": [
        {
          "regulation": "Utah Social Media Act",
          "reasoning": "Age collection detected but lacks the robust verification mechanism required for minors accessing social features.",
          "risk_level": "HIGH"
        }
      ],
      "requires_review": [
        {
          "regulation": "GDPR Article 8",
          "reasoning": "Age verification present but mechanism clarity needed for parental consent requirements.",
          "risk_level": "MEDIUM"
        }
      ]
    },
    "key_risks": [
      "Utah age verification gap could result in regulatory action",
      "GDPR consent flow may need parental approval enhancement",
      "Inconsistent geographic treatment across jurisdictions"
    ],
    "recommendations": [
      {
        "priority": "HIGH",
        "title": "Implement Document-Based Age Verification",
        "description": "Add document upload or credit card verification for Utah users under 18",
        "effort_estimate": "2-3 weeks development",
        "business_impact": "Required for Utah market compliance",
        "technical_approach": "Integrate third-party age verification service with geographic routing"
      },
      {
        "priority": "MEDIUM", 
        "title": "Enhance GDPR Consent Flow",
        "description": "Clarify parental consent mechanism for EU users under 16",
        "effort_estimate": "1-2 weeks",
        "business_impact": "Reduces GDPR audit risk"
      }
    ]
  },
  "confidence_assessment": {
    "overall_confidence": 0.87,
    "explanation_quality": "HIGH",
    "recommendation_actionability": "HIGH",
    "regulatory_accuracy": "VERIFIED"
  }
}
```

---

### `cds pipeline` - End-to-End Analysis

Execute the complete compliance detection pipeline from scanning to reporting.

#### Syntax

```powershell
cds pipeline --repo PATH --features LIST [OPTIONS]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--repo, -r` | Path | ✅ | Repository to analyze |
| `--features, -f` | String | ✅ | Comma-separated feature names |
| `--output-dir, -o` | Path | ❌ | Output directory |
| `--formats` | String | ❌ | Output formats: csv,html,json |
| `--probe-url` | URL | ❌ | URL for runtime probing |
| `--batch-size` | Integer | ❌ | Features to process in parallel |
| `--skip-runtime` | Boolean | ❌ | Skip runtime probing phase |
| `--skip-llm` | Boolean | ❌ | Skip LLM explanation phase |
| `--config` | Path | ❌ | Pipeline configuration file |

#### Examples

**Basic Usage:**
```powershell
# Analyze multiple features
cds pipeline --repo ./my-app --features user_registration,content_upload,payments
```

**Advanced Usage:**
```powershell
# Full pipeline with runtime probing
cds pipeline -r ./my-app -f user_auth,messaging --probe-url https://staging.myapp.com --formats csv,html,json

# Fast static-only analysis
cds pipeline --repo ./my-app --features all --skip-runtime --skip-llm --batch-size 5
```

#### Pipeline Configuration

```yaml
# pipeline_config.yml
pipeline:
  phases:
    static_analysis:
      enabled: true
      timeout: 300
      parallel_jobs: 4
    
    runtime_probing:
      enabled: true
      personas: ["us_utah_minor", "eu_adult", "ca_teen"]
      timeout: 60
      
    rules_evaluation:
      enabled: true
      regulations: ["utah_social_media", "coppa", "gdpr_article8"]
      confidence_threshold: 0.7
      
    llm_analysis:
      enabled: true
      model: "gemini-1.5-pro"
      temperature: 0.1
      max_tokens: 4096
      
    report_generation:
      formats: ["csv", "html"]
      template: "compliance_dashboard"

features:
  user_registration:
    paths: ["auth/", "registration/", "users/"]
    compliance_areas: ["age_verification", "data_collection"]
    
  content_moderation:
    paths: ["moderation/", "content/", "safety/"]
    compliance_areas: ["ncmec_reporting", "harmful_content"]
```

#### Output Files

The pipeline generates multiple output files:

```
artifacts/
├── pipeline_results.csv          # Structured data export
├── pipeline_report.html          # Interactive dashboard  
├── pipeline_data.json            # Complete analysis data
├── evidence/                     # Individual evidence files
│   ├── user_registration_evidence.json
│   ├── content_upload_evidence.json
│   └── payments_evidence.json
├── evaluations/                  # Rules evaluation results
│   ├── user_registration_evaluation.json
│   └── content_upload_evaluation.json
└── explanations/                 # LLM analysis results
    ├── user_registration_explanation.json
    └── content_upload_explanation.json
```

#### Progress Output

```
🔄 Starting CDS Pipeline...

🔍 Phase 1: Static Analysis (3 features)
┌─────────────────────┬─────────┬────────┬─────────────────┐
│ Feature             │ Status  │ Time   │ Signals Found   │
├─────────────────────┼─────────┼────────┼─────────────────┤
│ user_registration   │ ✅ Done  │ 8.2s   │ 7 signals       │
│ content_upload      │ ✅ Done  │ 12.1s  │ 12 signals      │
│ payments            │ ✅ Done  │ 5.4s   │ 3 signals       │
└─────────────────────┴─────────┴────────┴─────────────────┘

🧪 Phase 2: Runtime Probing (3 features)
┌─────────────────────┬─────────┬────────┬─────────────────┐
│ Feature             │ Status  │ Time   │ Personas Tested │
├─────────────────────┼─────────┼────────┼─────────────────┤
│ user_registration   │ ✅ Done  │ 45.2s  │ 5 personas      │
│ content_upload      │ ⚠️ Partial │ 60.0s  │ 4/5 personas    │
│ payments            │ ❌ Skip  │ 0.0s   │ Not testable    │
└─────────────────────┴─────────┴────────┴─────────────────┘

⚖️ Phase 3: Compliance Evaluation (3 features)
✅ 21 rules applied across 3 features
✅ Overall compliance score: 0.84

🤖 Phase 4: LLM Analysis (3 features)  
✅ Generated explanations and recommendations

📊 Phase 5: Report Generation
✅ CSV exported: artifacts/pipeline_results.csv
✅ HTML report: artifacts/pipeline_report.html
✅ JSON data: artifacts/pipeline_data.json

🎉 Pipeline completed in 2m 15s

📈 Results Summary:
• Features analyzed: 3
• Compliance issues found: 5 (2 high priority)
• Recommendations generated: 8
• Estimated remediation effort: 6-8 weeks
```

---

### `cds version` - System Information

Display version information and system diagnostics.

#### Syntax

```powershell
cds version [OPTIONS]
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `--diagnostics` | Boolean | Show detailed system information |
| `--dependencies` | Boolean | List installed dependencies |
| `--check-health` | Boolean | Test external integrations |

#### Examples

```powershell
# Basic version info
cds version

# Full system diagnostics
cds version --diagnostics --dependencies --check-health
```

#### Output Format

```
🔧 CDS Version Information

Version: 1.0.0
Build: 2024.12.15.1834
Python: 3.11.7 (main, Dec 15 2023, 12:09:04) [MSC v.1916 64 bit (AMD64)]
Platform: Windows-10-10.0.22631-SP0

📦 Core Dependencies:
✅ typer 0.9.0
✅ rich 13.7.0
✅ pydantic 2.5.2  
✅ pandas 2.1.4
✅ jinja2 3.1.2
✅ sqlmodel 0.0.14

🔍 Scanner Dependencies:
⚠️ semgrep - not installed (using mock implementation)
  Installation: pip install semgrep
✅ tree-sitter 0.20.4
✅ tree-sitter-python 0.20.4

🧪 Runtime Dependencies:
⚠️ playwright - not installed (using mock implementation)  
  Installation: pip install playwright && playwright install chromium
✅ httpx 0.25.2

🤖 LLM Dependencies:
⚠️ google-cloud-aiplatform - not installed
  Installation: pip install google-cloud-aiplatform
  Configuration: Set GOOGLE_APPLICATION_CREDENTIALS
✅ httpx 0.25.2 (for API requests)

💾 Database:
✅ SQLite 3.42.0 (built-in)
✅ Database file: D:\TIk Tok Hackathon\compliance-detection-system\evidence.db
✅ Tables: 3 (evidence_packs, rule_results, llm_analyses)

🏥 Health Check:
✅ Configuration valid
✅ Rules directory accessible (7 regulation files)
✅ Output directory writable  
⚠️ Semgrep unavailable (mock mode active)
⚠️ Playwright unavailable (mock mode active)
❌ Gemini API not configured

💡 Recommendations:
• Run: pip install semgrep playwright google-cloud-aiplatform
• Configure: Set GOOGLE_APPLICATION_CREDENTIALS for Gemini API
• Test: Run 'cds pipeline --repo . --features demo' to verify installation
```

## 📥📤 Input/Output Formats

### Input File Formats

#### Evidence Pack JSON
```json
{
  "feature_name": "string",
  "repo": "string",  
  "timestamp": "ISO 8601 datetime",
  "static_signals": { /* StaticSignals schema */ },
  "runtime_signals": { /* RuntimeSignals schema */ },
  "metadata": { /* EvidenceMetadata schema */ }
}
```

#### Personas JSON
```json
{
  "personas": [
    {
      "id": "string",
      "country": "ISO 3166-1 alpha-2",
      "age": "integer (0-150)",
      "language": "IETF language tag",
      "timezone": "IANA timezone",
      "test_scenarios": ["array of strings"]
    }
  ]
}
```

#### Rules JSON
```json
{
  "rules": [
    {
      "name": "string",
      "regulation_id": "string", 
      "description": "string",
      "logic": { /* JSON Logic expression */ },
      "confidence_factors": { /* key-value pairs */ },
      "priority": "LOW|MEDIUM|HIGH|CRITICAL"
    }
  ]
}
```

### Output File Formats

#### CSV Export Schema
| Column | Type | Description |
|--------|------|-------------|
| `feature_name` | String | Feature identifier |
| `analysis_timestamp` | DateTime | When analysis was performed |
| `overall_verdict` | Enum | COMPLIANT, NON_COMPLIANT, REQUIRES_REVIEW, NOT_APPLICABLE |
| `confidence_score` | Float | Overall confidence (0.0-1.0) |
| `risk_level` | Enum | LOW, MEDIUM, HIGH, CRITICAL |
| `regulations_tested` | Integer | Number of regulations evaluated |
| `compliant_regulations` | Integer | Number passing compliance |
| `non_compliant_regulations` | Integer | Number failing compliance |
| `evidence_quality_score` | Float | Evidence completeness (0.0-1.0) |
| `static_signals_count` | Integer | Number of static signals found |
| `runtime_signals_count` | Integer | Number of runtime signals found |
| `high_priority_recommendations` | Integer | Number of high priority actions |
| `estimated_effort_weeks` | Integer | Estimated remediation effort |
| `primary_recommendation` | String | Top recommendation summary |
| `regulatory_references` | String | Comma-separated regulation IDs |

#### HTML Report Structure
```html
<!DOCTYPE html>
<html>
<head>
    <title>CDS Compliance Report</title>
    <!-- Bootstrap CSS for styling -->
</head>
<body>
    <!-- Executive Summary Dashboard -->
    <div id="executive-summary">
        <!-- Compliance score gauge, risk distribution chart -->
    </div>
    
    <!-- Feature-by-Feature Analysis -->
    <div id="feature-analysis">
        <!-- Expandable cards for each feature -->
    </div>
    
    <!-- Regulatory Coverage Matrix -->
    <div id="regulatory-matrix">
        <!-- Heatmap of feature vs regulation compliance -->
    </div>
    
    <!-- Recommendations Timeline -->
    <div id="recommendations">
        <!-- Prioritized action items with effort estimates -->
    </div>
    
    <!-- Technical Details -->
    <div id="technical-details">
        <!-- Evidence details, confidence explanations -->
    </div>
</body>
</html>
```

## 🚪 Exit Codes

CDS commands return standardized exit codes for script automation:

| Code | Status | Description |
|------|--------|-------------|
| `0` | Success | Command completed successfully |
| `1` | General Error | Invalid arguments, file not found, etc. |
| `2` | Analysis Error | Scanner/analyzer failure |
| `3` | Partial Success | Some components failed but results available |
| `4` | Configuration Error | Invalid config file, missing API keys |
| `5` | Network Error | Unable to reach external services |
| `6` | Timeout Error | Operation exceeded time limit |

### Exit Code Usage Examples

```powershell
# Check if scan was successful
cds scan --repo . --feature test
if ($LASTEXITCODE -eq 0) {
    Write-Output "Scan completed successfully"
} elseif ($LASTEXITCODE -eq 3) {
    Write-Output "Partial results available, check logs"
} else {
    Write-Output "Scan failed with exit code: $LASTEXITCODE"
    exit $LASTEXITCODE
}

# Pipeline automation with error handling
cds pipeline --repo . --features user_auth,content_upload
switch ($LASTEXITCODE) {
    0 { Write-Output "✅ Pipeline completed successfully" }
    3 { Write-Output "⚠️ Pipeline completed with warnings" }
    default { 
        Write-Output "❌ Pipeline failed: $LASTEXITCODE"
        exit $LASTEXITCODE
    }
}
```

## 🌍 Environment Variables

Configure CDS behavior through environment variables:

### Core Configuration
```powershell
# Logging
$env:CDS_LOG_LEVEL = "INFO"                    # DEBUG, INFO, WARNING, ERROR
$env:CDS_LOG_FORMAT = "detailed"               # simple, detailed, json

# Output
$env:CDS_OUTPUT_DIR = "compliance_reports"     # Default output directory
$env:CDS_OUTPUT_FORMAT = "csv,html"            # Default export formats
$env:CDS_ARTIFACTS_RETENTION_DAYS = "30"       # Auto-cleanup old artifacts

# Performance  
$env:CDS_MAX_PARALLEL_JOBS = "4"               # Parallel processing jobs
$env:CDS_MEMORY_LIMIT_MB = "2048"              # Memory usage limit
$env:CDS_TIMEOUT_SECONDS = "1800"              # Global operation timeout
```

### Scanner Configuration
```powershell
# Static Analysis
$env:CDS_SEMGREP_TIMEOUT = "300"               # Semgrep timeout in seconds
$env:CDS_SEMGREP_MEMORY_LIMIT = "4096"         # Semgrep memory limit (MB)  
$env:CDS_TREESITTER_CACHE_DIR = "~/.cds/cache" # AST parsing cache directory
$env:CDS_SCANNER_RULES_DIR = "custom_rules/"   # Custom scanning rules

# Runtime Probing
$env:CDS_PLAYWRIGHT_TIMEOUT = "30000"          # Playwright timeout (ms)
$env:CDS_PLAYWRIGHT_HEADLESS = "true"          # Headless browser mode
$env:CDS_PROBE_RETRIES = "3"                   # Retry failed probes
$env:CDS_PROBE_PARALLEL_SESSIONS = "3"         # Concurrent browser sessions
```

### LLM Integration
```powershell
# Google Cloud / Gemini
$env:GOOGLE_CLOUD_PROJECT = "my-project-id"    # GCP Project ID
$env:GOOGLE_CLOUD_REGION = "us-central1"       # GCP Region
$env:GOOGLE_APPLICATION_CREDENTIALS = "path/to/service-account.json"

# LLM Configuration
$env:CDS_LLM_MODEL = "gemini-1.5-pro"          # Model selection
$env:CDS_LLM_TEMPERATURE = "0.1"               # Response randomness (0.0-1.0)
$env:CDS_LLM_MAX_TOKENS = "4096"               # Maximum response length
$env:CDS_LLM_RATE_LIMIT = "10"                 # Requests per minute
$env:CDS_LLM_CACHE_ENABLED = "true"            # Enable response caching
```

### Database Configuration
```powershell
# SQLite (default)
$env:CDS_DATABASE_URL = "sqlite:///cds.db"     # Database connection string
$env:CDS_DB_BACKUP_ENABLED = "true"            # Enable automatic backups
$env:CDS_DB_BACKUP_INTERVAL = "24"             # Backup interval (hours)

# PostgreSQL (enterprise)
$env:CDS_DATABASE_URL = "postgresql://user:pass@host:5432/cds"
$env:CDS_DB_POOL_SIZE = "20"                   # Connection pool size
$env:CDS_DB_MAX_OVERFLOW = "30"                # Max overflow connections
```

### Feature Flags
```powershell
# Experimental Features
$env:CDS_ENABLE_EXPERIMENTAL_FEATURES = "false" # Enable beta features
$env:CDS_ENABLE_ML_CONFIDENCE = "false"         # ML confidence prediction
$env:CDS_ENABLE_INCREMENTAL_SCAN = "true"       # Git-based incremental scanning

# Development/Testing
$env:CDS_MOCK_EXTERNAL_SERVICES = "false"       # Force mock implementations
$env:CDS_SKIP_VERSION_CHECK = "false"           # Skip dependency version validation
$env:CDS_DEBUG_EVIDENCE_VALIDATION = "false"    # Extra evidence validation
```

## ⚙️ Configuration Files

### Main Configuration File (`cds_config.yml`)

```yaml
# cds_config.yml - Main configuration file
version: "1.0"

# Logging configuration
logging:
  level: INFO                    # DEBUG, INFO, WARNING, ERROR
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "cds.log"                # Log file path (optional)
  max_file_size: "10MB"          # Log rotation size
  backup_count: 5                # Number of backup files

# Output configuration  
output:
  directory: "artifacts"         # Base output directory
  formats: ["csv", "html"]       # Default export formats
  retention_days: 30             # Automatic cleanup
  templates:
    html: "compliance_dashboard"  # HTML template selection
    csv: "standard_export"       # CSV template selection

# Scanner configuration
scanner:
  timeout: 300                   # Global scanner timeout (seconds)
  parallel_jobs: 4               # Concurrent scanning jobs
  rules_directories:             # Custom rules locations
    - "data/rules"
    - "organization/compliance_rules"
  exclude_patterns:              # Global exclusion patterns
    - "node_modules"
    - "*.git"
    - "build"
    - "dist"

# Runtime probing configuration
runtime:
  enabled: true                  # Enable runtime probing
  timeout: 30                    # Per-probe timeout (seconds)
  retry_attempts: 3              # Failed probe retries
  default_personas: "data/personas/default.json"
  browsers:
    - chromium                   # Primary browser
    - firefox                    # Fallback browser
  viewport: "1920x1080"          # Default viewport size
  
# Rules engine configuration  
rules:
  confidence_threshold: 0.7      # Minimum confidence for positive verdicts
  regulations:                   # Default regulations to apply
    - "utah_social_media"
    - "coppa"
    - "gdpr_article8"
    - "ncmec_reporting"
  custom_rules_directory: "organization/rules"
  validation_enabled: true       # Validate rules on startup

# LLM integration configuration
llm:
  provider: "gemini"             # gemini, openai, anthropic
  model: "gemini-1.5-pro"        # Model selection
  temperature: 0.1               # Response randomness
  max_tokens: 4096               # Maximum response length
  cache_enabled: true            # Enable response caching
  cache_ttl: 3600                # Cache TTL in seconds
  rate_limit: 10                 # Requests per minute
  
# Database configuration
database:
  url: "sqlite:///evidence.db"   # Connection string
  backup_enabled: true           # Enable automatic backups
  backup_interval: 24            # Backup frequency (hours)
  retention_days: 90             # Data retention period

# Performance tuning
performance:
  max_memory_mb: 2048            # Memory usage limit
  max_concurrent_operations: 4   # Concurrent pipeline operations
  enable_caching: true           # Enable various caches
  cache_directory: "~/.cds/cache"

# Feature flags
features:
  experimental_ml: false         # ML-enhanced confidence scoring
  incremental_scanning: true     # Git-based incremental analysis
  advanced_reporting: false      # Beta reporting features
  
# Organization-specific settings
organization:
  name: "My Organization"        # Organization name for reports
  compliance_contact: "compliance@myorg.com"
  legal_disclaimer: true         # Include legal disclaimers in reports
  custom_branding: true          # Use organization branding in HTML reports
```

### Pipeline Configuration (`pipeline_config.yml`)

```yaml
# pipeline_config.yml - Pipeline-specific configuration
pipeline:
  name: "Standard Compliance Pipeline"
  version: "1.0"
  
  # Pipeline phases configuration
  phases:
    static_analysis:
      enabled: true
      timeout: 300
      parallel_jobs: 4
      rules_directories:
        - "data/rules"
        - "custom/semgrep_rules"
      
    runtime_probing:
      enabled: true  
      personas: ["us_utah_minor", "eu_adult", "ca_teen", "au_minor", "uk_adult"]
      timeout: 60
      retry_attempts: 2
      
    rules_evaluation:
      enabled: true
      regulations:
        - "utah_social_media_2024"
        - "coppa_child_protection"  
        - "gdpr_article8"
        - "ncmec_reporting"
        - "eu_dsa_transparency"
        - "ca_privacy_act"
      confidence_threshold: 0.7
      
    llm_analysis:
      enabled: true
      model: "gemini-1.5-pro"
      temperature: 0.1
      max_tokens: 4096
      explanation_style: "technical"  # technical, executive, legal
      
    report_generation:
      formats: ["csv", "html", "json"]
      templates:
        html: "compliance_dashboard"
      include_recommendations: true
      include_evidence_details: true

# Feature definitions
features:
  user_registration:
    description: "User account creation and profile setup"
    paths:                       # Code paths to analyze
      - "auth/"
      - "registration/"  
      - "users/"
    exclude_paths:               # Paths to exclude
      - "auth/legacy/"
    compliance_areas:            # Expected compliance areas
      - "age_verification"
      - "data_collection"
      - "geo_compliance"
    test_scenarios:              # Runtime test scenarios
      - "registration_flow"
      - "age_verification"
      - "social_features_access"
      
  content_moderation:
    description: "User-generated content review and safety"
    paths:
      - "moderation/"
      - "content/"
      - "safety/"
    compliance_areas:
      - "ncmec_reporting"
      - "harmful_content"
      - "age_appropriate_content"
    test_scenarios:
      - "content_upload"
      - "reporting_flow"
      - "moderation_actions"
      
  recommendation_engine:
    description: "Personalized content and user recommendations"
    paths:
      - "recommendations/"
      - "ml/"
      - "personalization/"
    compliance_areas:
      - "algorithmic_transparency"  
      - "filter_bubbles"
      - "age_appropriate_recommendations"
    test_scenarios:
      - "recommendation_generation"
      - "preference_learning"
      - "content_filtering"

# Reporting configuration
reporting:
  executive_summary:
    include_risk_assessment: true
    include_effort_estimates: true
    include_regulatory_summary: true
    
  technical_details:
    include_evidence_breakdown: true
    include_confidence_analysis: true
    include_rule_explanations: true
    
  recommendations:
    prioritization: "risk_and_effort"  # risk, effort, risk_and_effort
    include_implementation_guidance: true
    include_testing_approaches: true
    
  branding:
    organization_logo: "assets/logo.png"
    primary_color: "#1f4e79"
    report_footer: "Generated by CDS - Compliance Detection System"
```

---

**📝 Last Updated**: December 2024  
**🔄 CLI Version**: 1.0.0  
**📖 Related Docs**: [User Manual](../guides/user-manual.md) | [System Architecture](../architecture/system-overview.md)

This CLI reference provides complete documentation for all CDS commands, options, and configuration. For additional help, use `cds COMMAND --help` or visit our [troubleshooting guide](../guides/user-manual.md#troubleshooting).
