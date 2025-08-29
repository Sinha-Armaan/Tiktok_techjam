# CDS - Compliance Detection System 

> **MVP for detecting geo-specific compliance requirements in code features using static analysis + runtime probes + LLM reasoning**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git
- (Optional) Google Cloud Project with Vertex AI enabled

### 1-Command Demo

```bash
# Clone and setup
git clone <your-repo-url> && cd compliance-detection-system

# Install dependencies (using pip)
pip install -e .

# Set up environment
cp .env.example .env
# Edit .env with your Google Cloud project details (optional for demo)

# Run the complete pipeline
cds pipeline --dataset ./data/sample_dataset.csv --output ./artifacts/final.csv --report ./artifacts/report.html
```

**Demo Output:**
- 📊 `./artifacts/final.csv` - Compliance analysis results
- 📋 `./artifacts/report.html` - Interactive HTML report
- 🗂️ `./artifacts/evidence/` - Detailed evidence files

### Testing with Dataset Variations

The system includes three specialized dataset variations with intentional compliance and security issues for testing:

#### 📋 Run with Original Comprehensive Dataset
```bash
# Test general compliance detection (COPPA, GDPR, Utah Act)
python demo_pipeline.py original_comprehensive_focused

# Features: User registration, content recommendation, crisis intervention
# Focus: General compliance with intentional gaps
```

#### 🔒 Run with Enterprise Security Dataset
```bash
# Test enterprise security vulnerability detection
python demo_pipeline.py enterprise_security_focused

# Features: Threat detection, zero trust, IAM, security monitoring
# Focus: Security vulnerabilities and enterprise compliance gaps
```

#### 🌍 Run with Global Expansion Dataset
```bash
# Test international compliance and data sovereignty
python demo_pipeline.py global_expansion_focused

# Features: Multi-region compliance, localization, cross-border transfers
# Focus: International regulations (GDPR, CCPA, PIPEDA, LGPD)
```

#### 🎯 What These Datasets Test
Each dataset contains **intentional issues** for validation:

**PRD-Level Issues:**
- Missing age verification or COPPA compliance gaps
- Inadequate data retention/deletion policies  
- Missing consent management details
- Insufficient privacy disclosures

**TRD-Level Issues:**
- Missing input validation (SQL injection risks)
- Weak authentication/authorization mechanisms
- Insecure data handling practices
- Inadequate error handling exposing sensitive data

**Code-Level Issues:**
- Hardcoded secrets, API keys, passwords
- SQL injection vulnerabilities
- Missing authentication on sensitive endpoints
- Weak encryption or plaintext PII storage

#### 📊 Expected Results
- **Original Comprehensive**: 3 features processed, multiple compliance gaps detected
- **Enterprise Security**: 4 features processed, security vulnerabilities flagged
- **Global Expansion**: 4 features processed, international compliance issues found

All results include:
- 📈 **CSV Results**: `artifacts/comprehensive_demo_results.csv`
- 🌐 **HTML Report**: `artifacts/comprehensive_demo_report.html` 
- 📁 **Evidence Files**: `artifacts/evidence/` directory
- 🚩 **Issue Detection**: Known vulnerabilities flagged with `needs_review=True`

#### 🔍 Generating Evidence Files (Required)

Before running the pipeline, generate evidence files from the dataset artifacts:

```bash
# Generate evidence files for all dataset variations
python generate_evidence.py

# This creates evidence JSON files in artifacts/evidence/
# Required for the pipeline to analyze the intentional issues
```

The evidence generator:
- ✅ Creates evidence files for all 11 features across 3 dataset variations
- ✅ Extracts content from PRDs, TRDs, and implementation code  
- ✅ Pre-analyzes artifacts for compliance and security issues
- ✅ Enables the pipeline to detect intentional vulnerabilities

#### 📁 Dataset Variations Structure
```
dataset_variations/
├── original_comprehensive_focused/    # General compliance (3 features)
├── enterprise_security_focused/       # Security-focused (4 features)  
└── global_expansion_focused/          # International (4 features)
```

Each variation contains:
- 📊 **Feature datasets** (CSV files with metadata)
- 📄 **Comprehensive artifacts** (PRDs, TRDs, design docs)
- 💻 **Implementation code** (with intentional vulnerabilities)
- 🎯 **Intentional issues** for testing compliance detection

### ⚡ Quick Reference

```bash
# 1. Generate evidence files (run once)
python generate_evidence.py
# Creates evidence files for all 11 features across 3 dataset variations

# 2. Test with different datasets
python demo_pipeline.py original_comprehensive_focused    # General compliance
python demo_pipeline.py enterprise_security_focused       # Security vulnerabilities  
python demo_pipeline.py global_expansion_focused          # International compliance

# 3. View results
start artifacts/comprehensive_demo_report.html             # HTML report (Windows)
open artifacts/comprehensive_demo_report.html              # HTML report (Mac/Linux)  
code artifacts/comprehensive_demo_results.csv              # CSV results
```

**Expected Output per Run:**
- 📊 3-4 features processed (varies by dataset)
- 🚩 Multiple intentional issues detected  
- 📋 Detailed evidence files generated
- 🎯 All features flagged for manual review (`needs_review=True`)
- ⚡ Uses existing compliance rules from `./data/rules/compliance_rules.json`

## 🏗️ Architecture

```
┌─ Static Scanner ─┐    ┌─ Runtime Probes ─┐    ┌─ Rules Engine ─┐
│  • Semgrep       │    │  • Playwright     │    │  • JSON Logic  │
│  • Tree-sitter   │ -> │  • Personas       │ -> │  • Confidence  │
│  • AST Analysis  │    │  • UI States      │    │  • Regulations │
└───────────────────┘    └───────────────────┘    └────────────────┘
           │                        │                        │
           └────────────────────────┼────────────────────────┘
                                    ↓
              ┌────────────── Evidence Pack ──────────────┐
              │  Static + Runtime + Metadata + Files     │
              └─────────────────┬─────────────────────────┘
                                ↓
                    ┌─── LLM Analysis (Gemini 1.5) ───┐
                    │  • Compliance Reasoning          │
                    │  • Regulatory Mapping           │ 
                    │  • Confidence Scoring           │
                    └─────────────┬───────────────────┘
                                  ↓
                         ┌─ Final Record ─┐
                         │  CSV + HTML    │
                         │   Reports      │
                         └────────────────┘
```

## 🛠️ Core Commands

### Static Analysis
```bash
# Scan repository for compliance patterns
cds scan --repo ./sample_repo --feature user_registration

# Output: ./artifacts/evidence/user_registration.json
```

### Runtime Probing
```bash
# Test with different personas
cds probe --persona ut_minor --url http://localhost:3000 --feature live_test

# Available personas: ut_minor, fr_adult, ca_teen, uk_adult
```

### Rules Evaluation
```bash
# Apply compliance rules to evidence
cds evaluate --feature user_registration

# Uses: JSON Logic rules from ./data/rules/compliance_rules.json
```

### LLM Explanation
```bash
# Generate AI-powered compliance analysis
cds explain --feature user_registration

# Output: Detailed reasoning + regulatory mapping
```

### Batch Processing
```bash
# Process entire dataset
cds pipeline --dataset ./data/sample_dataset.csv
```

## 📊 What Gets Detected

### Static Analysis Signals
- **🌍 Geographic Branching**: Country lists, region checks
- **👶 Age Verification**: Age gate imports, minor checks  
- **🏠 Data Residency**: Region configurations, storage locations
- **📋 Reporting Clients**: NCMEC, CSAM detection systems
- **🚩 Feature Flags**: Compliance-related toggles
- **👨‍👩‍👧‍👦 Parental Controls**: Consent systems, restrictions

### Runtime Probe Signals  
- **🎭 Persona Testing**: ut_minor (UT, 16), fr_adult (FR, 25)
- **🚫 Blocked Actions**: Age-restricted features, geo-blocks
- **🖥️ UI States**: Cookie banners, consent modals, privacy settings
- **🏁 Feature Flags**: Runtime flag resolutions
- **🌐 Network Traces**: API calls, data residency patterns

### Compliance Rules Detected
- **Utah Social Media Act**: Minor curfew enforcement (10:30 PM - 6:30 AM)
- **NCMEC Reporting**: Mandatory CSAM reporting requirements
- **EU DSA**: Transparency reports, user flagging, appeals
- **GDPR**: Lawful basis, data subject rights, privacy by design
- **COPPA**: Parental consent for children under 13
- **State Privacy Laws**: Default-off privacy features for minors

## 🔧 Configuration

### Environment Variables
```bash
# Required for LLM analysis (optional for demo)
GOOGLE_CLOUD_PROJECT=your-project-id
GEMINI_LOCATION=us-central1

# Optional configurations
DATA_DIR=./data
ARTIFACT_DIR=./artifacts
LOG_LEVEL=INFO
```

### Custom Rules
Add rules to `./data/rules/compliance_rules.json`:

```json
{
  "id": "CUSTOM_RULE",
  "name": "My Custom Compliance Rule",
  "logic": {
    "and": [
      {"==": [{"var": "static.pf_controls"}, true]},
      {"<": [{"var": "runtime.persona.age"}, 18]}
    ]
  },
  "requires_controls": ["age_verification"],
  "regulations": ["My Regulation"],
  "severity": "medium"
}
```

### Custom Semgrep Rules
Extend `./data/rules/semgrep.yml`:

```yaml
- id: my-compliance-pattern
  pattern: my_compliance_function(...)
  message: "Custom compliance pattern detected"
  languages: [python, javascript]
  severity: INFO
```

## 📁 Project Structure

```
compliance-detection-system/
├── cds/                    # Main package
│   ├── cli/               # CLI interface (Typer)
│   ├── scanner/           # Static analysis (Semgrep + Tree-sitter)
│   ├── runtime/           # Playwright probing
│   ├── rules/             # JSON Logic rules engine  
│   ├── llm/               # Gemini 1.5 integration
│   └── evidence/          # Data models + pipeline
├── data/                  # Configuration & rules
│   ├── rules/            # Semgrep + JSON Logic rules
│   ├── policy_snippets.json  # Regulatory text snippets
│   └── sample_dataset.csv    # Demo dataset
├── sample_repo/           # Demo repository with compliance patterns
├── artifacts/             # Output directory
│   ├── evidence/         # Evidence JSON files
│   ├── final.csv         # Results export
│   └── report.html       # HTML report
└── scripts/              # Utility scripts
```

## 🧪 Development

### Setup Development Environment
```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy cds/

# Code formatting
ruff format cds/
ruff check cds/
```

### Adding New Scanners
```python
# cds/scanner/my_scanner.py
class MyScanner:
    def scan(self, repo_path: Path) -> Dict[str, List[Dict]]:
        # Your custom scanning logic
        return {"my_signal_type": [{"file": "test.py", "line": 1}]}
```

### Adding New Rules
```python
# Add to compliance_rules.json
{
  "id": "MY_RULE",
  "logic": {"==": [{"var": "static.my_signal"}, true]},
  "requires_controls": ["my_control"],
  "regulations": ["My Regulation"]
}
```

## 📊 Sample Output

### CSV Export Format
```csv
feature_id,requires_geo_logic,reasoning,confidence,severity
user_registration,true,"Geographic branching detected with countries US;CA;EU and age verification systems",0.85,high
content_recommendation,true,"NCMEC reporting client detected with recommendation system flags",0.92,critical
```

### HTML Report
Interactive report with:
- 📈 Summary statistics dashboard
- 🔍 Feature-by-feature analysis  
- 📋 Regulatory requirements mapping
- 🔗 Code reference links
- ⚠️ Review recommendations

## 🚀 Deployment

### Docker
```bash
# Build image
docker build -t cds .

# Run pipeline
docker run -v $(pwd)/data:/data -v $(pwd)/artifacts:/artifacts cds \
  pipeline --dataset /data/sample_dataset.csv
```

### CI/CD (GitHub Actions)
```yaml
- name: Run Compliance Detection
  run: |
    pip install -e .
    cds pipeline --dataset ./data/production_dataset.csv
    
- name: Upload Results
  uses: actions/upload-artifact@v3
  with:
    name: compliance-results
    path: artifacts/
```

## 🎯 Success Metrics

### MVP Completion ✅
- [x] All CLI commands functional
- [x] End-to-end pipeline produces valid CSV
- [x] HTML reports render with evidence links  
- [x] Demo completes in under 3 minutes

### Quality Indicators ⚡
- [x] Static analysis detects 6+ compliance patterns
- [x] Rules engine evaluates 7+ regulatory requirements
- [x] LLM integration provides detailed reasoning
- [x] Pipeline processes 10+ features reliably

### Scalability Ready 📈
- [x] SQLite-based registry (Postgres-ready)
- [x] Modular scanner architecture
- [x] Cloud-ready LLM integration
- [x] Extensible rules framework

## 📜 Supported Regulations

| Regulation | Jurisdiction | Coverage | Severity |
|------------|-------------|----------|----------|
| **Utah Social Media Act** | Utah, USA | Minor curfew restrictions | High |
| **NCMEC Reporting** | United States | CSAM mandatory reporting | Critical |
| **EU Digital Services Act** | European Union | Transparency & appeals | High |  
| **GDPR** | EU/EEA/UK | Data subject rights | High |
| **COPPA** | United States | Children under 13 | Critical |
| **CCPA** | California, USA | Consumer privacy rights | Medium |
| **UK Age Appropriate Design** | United Kingdom | Child safety by design | High |
| **Texas HB 18** | Texas, USA | Minor privacy defaults | Medium |

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-scanner`
3. **Add your code**: Follow existing patterns in `cds/`
4. **Write tests**: Add to `tests/` directory
5. **Submit PR**: Include demo output and documentation

### Contribution Areas
- 🔍 **New Scanners**: AST patterns, regex rules, API integrations
- ⚖️ **Compliance Rules**: New jurisdictions, regulatory updates
- 🎭 **Runtime Probes**: Additional personas, test scenarios
- 🤖 **LLM Improvements**: Prompt engineering, fallback logic
- 📊 **Reporting**: New export formats, visualizations

## 📞 Support

- 📖 **Documentation**: See `docs/` directory
- 🐛 **Issues**: GitHub Issues for bugs and features  
- 💬 **Discussions**: GitHub Discussions for questions
- 📧 **Contact**: team@cds.dev

## 📄 License

MIT License - see `LICENSE` file for details.

## 🙏 Acknowledgments

- **Semgrep**: Static analysis rules engine
- **Playwright**: Runtime browser automation
- **Google Vertex AI**: LLM analysis capabilities  
- **JSON Logic**: Flexible rules evaluation
- **TikTok Hackathon**: Inspiration and opportunity

---

**Built with ❤️ for compliance automation**

*CDS v0.1.0 - Detect compliance requirements before they become problems*
