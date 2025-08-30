# CDS - Compliance Detection System 

> **Production-ready system for detecting geo-specific compliance requirements in TikTok features using static analysis + LLM reasoning + gray area detection**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Compliance Ready](https://img.shields.io/badge/compliance-ready-green.svg)](https://github.com/Sinha-Armaan/Tiktok_techjam)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git
- Google AI Studio API key (free)

### 2-Command Demo

```powershell
# Navigate to project
cd "C:\Users\iidab\OneDrive\Desktop\Tiktok\Tiktok_techjam\compliance-detection-system"

# Run the complete compliance detection pipeline
python demo_pipeline.py original_comprehensive_focused
```

**Demo Output:**
- 📊 `artifacts/comprehensive_demo_results.csv` - 9 features analyzed with confidence scores
- 📋 `artifacts/comprehensive_demo_report.html` - Interactive compliance dashboard
- 🗂️ `artifacts/evidence/` - 85+ detailed evidence files for audit trails

### Alternative: CLI Interface

The system also provides a professional CLI interface:

```powershell
# Use the CLI for pipeline analysis
cds pipeline --dataset "dataset_variations/original_comprehensive_focused/data/comprehensive_features_dataset.csv" --output "artifacts/cli_results.csv" --report "artifacts/cli_report.html"

# Scan individual features
cds scan --repo "dataset_variations/original_comprehensive_focused/enhanced_code" --feature "regional_content_block"

# Check system status
cds version
```

## 🎯 **Gray Area Compliance Detection**

CDS excels at detecting **nuanced compliance scenarios** with sophisticated confidence scoring:

### **Confidence Score Distribution**
- **0.0-0.1**: Clear non-compliance cases
- **0.4-0.69**: **Gray area** compliance (requires review)  
- **0.75-0.89**: High confidence compliance requirements
- **0.90-1.0**: Critical compliance requirements

### **Sample Gray Area Results**
```csv
feature_id,requires_geo_logic,confidence,reasoning
age_gated_messaging,True,0.8,"Geographic branching + unclear regulatory alignment"
regional_advertising_controls,True,0.75,"Partial implementation with missing controls"  
regional_content_block,True,0.9,"Clear geographic restrictions with data residency"
```

## 🔧 **Tested Dataset Variations**

The system includes production-ready test datasets with **intentional compliance scenarios**:

#### 📋 Original Comprehensive Dataset ✅ **TESTED**
```powershell
python demo_pipeline.py original_comprehensive_focused
```
**Features:** 9 total (3 standard + 6 ambiguous gray area cases)  
**Focus:** General compliance with nuanced scoring (COPPA, GDPR, Utah Act)  
**Gray Areas:** Age-gated messaging, regional advertising controls, cross-border data sharing

#### 🔒 Enterprise Security Dataset  
```powershell
python demo_pipeline.py enterprise_security_focused
```
**Features:** Security-focused compliance scenarios  
**Focus:** Enterprise vulnerabilities and security compliance gaps

#### 🌍 Global Expansion Dataset
```powershell
python demo_pipeline.py global_expansion_focused  
```
**Features:** International compliance scenarios  
**Focus:** Multi-jurisdictional regulations (GDPR, CCPA, PIPEDA, LGPD)

#### 🎯 **Validated Results**
Each dataset produces **comprehensive compliance analysis**:

**Standard Features:**
- `user_registration`: 0.0 confidence (clear non-compliance)
- `content_recommendation`: 0.1 confidence (minor issues detected)
- `crisis_intervention`: 0.1 confidence (well-implemented safety feature)

**Gray Area Features:**
- `regional_content_block`: 0.9 confidence (clear geo-compliance requirement)
- `age_gated_messaging`: **0.8 confidence** (perfect gray area example)
- `regional_advertising_controls`: **0.75 confidence** (compliance gaps detected)
- `cross_border_data_sharing`: 0.9 confidence (data residency requirements)

**Output Generated:**
- 📈 **CSV Results**: `artifacts/comprehensive_demo_results.csv` (9 features)
- 🌐 **HTML Report**: `artifacts/comprehensive_demo_report.html` (interactive dashboard)
- 📁 **Evidence Files**: `artifacts/evidence/` (85+ detailed JSON files)
- 🚩 **Regulatory Mapping**: GDPR, COPPA, CCPA, NCMEC requirements identified

## 🏗️ **Production Architecture**

```
┌─ Static Scanner ─┐    ┌─ LLM Analysis ─┐    ┌─ Rules Engine ─┐
│  • Semgrep       │    │  • Google AI   │    │  • JSON Logic  │
│  • Tree-sitter   │ -> │  • Confidence  │ -> │  • Regulations │
│  • AST Analysis  │    │  • Reasoning   │    │  • Evidence    │
└───────────────────┘    └────────────────┘    └────────────────┘
           │                        │                        │
           └────────────────────────┼────────────────────────┘
                                    ↓
              📊 Comprehensive Reports + Audit Trails
```

## 🛠️ **Core Commands Tested**

### **Python Script Interface** ✅ **VERIFIED**
```powershell
# Main pipeline command (most common usage)
python demo_pipeline.py original_comprehensive_focused

# Output: 9 features processed, gray area confidence scoring working
```

### **CLI Interface** ✅ **VERIFIED**  
```powershell
# Professional CLI pipeline
cds pipeline --dataset "dataset_variations/original_comprehensive_focused/data/comprehensive_features_dataset.csv" --output "artifacts/cli_results.csv" --report "artifacts/cli_report.html"

# Individual feature scanning
cds scan --repo "dataset_variations/original_comprehensive_focused/enhanced_code" --feature "regional_content_block"

# System diagnostics
cds version  # Shows: CDS v0.1.0, Python 3.13.3
cds --help   # Full command reference
```

## 📊 **What Gets Detected**

### **Static Analysis Signals** ✅ **WORKING**
- **🌍 Geographic Branching**: Country lists, region checks in code
- **👶 Age Verification**: Age gate imports, parental consent logic  
- **🏠 Data Residency**: Regional storage configurations, cross-border controls
- **📋 Reporting Clients**: NCMEC integration, CSAM detection systems
- **🚩 Feature Flags**: Compliance-related toggles and configurations
- **� Security Issues**: Hardcoded secrets, SQL injection vulnerabilities

### **LLM Analysis Results** ✅ **VALIDATED**  
- **🤖 Compliance Reasoning**: Detailed natural language explanations
- **⚖️ Regulatory Mapping**: Links to GDPR, COPPA, CCPA, NCMEC requirements
- **� Confidence Scoring**: 0.0-1.0 scale with gray area detection (0.4-0.69)
- **🔍 Missing Controls**: Identification of compliance gaps and needed implementations
- **📋 Evidence References**: Traceable links to code files and line numbers

### **Compliance Rules Detected** ✅ **TESTED**
- **Utah Social Media Act**: Minor curfew enforcement, parental controls
- **NCMEC Reporting**: Mandatory CSAM reporting requirements  
- **GDPR**: Data subject rights, lawful basis validation, cross-border transfers
- **COPPA**: Parental consent for children under 13
- **CCPA**: California consumer privacy rights, age-based advertising restrictions

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
