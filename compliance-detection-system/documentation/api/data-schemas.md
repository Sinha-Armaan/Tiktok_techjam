# Data Schemas Reference

Complete data schema documentation for the **Compliance Detection System (CDS)**. All input/output formats, validation rules, and data models.

## 📋 Table of Contents

1. [Core Data Models](#core-data-models)
2. [Input Schemas](#input-schemas)
3. [Output Schemas](#output-schemas)
4. [Configuration Schemas](#configuration-schemas)
5. [Validation Rules](#validation-rules)
6. [Schema Evolution](#schema-evolution)
7. [Examples](#examples)

## 🏗️ Core Data Models

CDS uses [Pydantic v2](https://docs.pydantic.dev/latest/) for data validation and serialization. All models include automatic validation, type checking, and JSON schema generation.

### EvidencePack Model

Central data structure containing all collected compliance evidence for a feature.

```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime

class EvidencePack(BaseModel):
    """Complete evidence package for a feature's compliance analysis"""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid',
        frozen=False
    )
    
    # Core identification
    feature_name: str = Field(
        description="Unique feature identifier",
        min_length=1,
        max_length=100,
        pattern=r"^[a-zA-Z][a-zA-Z0-9_-]*$"
    )
    
    repo: str = Field(
        description="Repository path or identifier",
        min_length=1,
        max_length=500
    )
    
    timestamp: datetime = Field(
        description="Evidence collection timestamp",
        default_factory=datetime.utcnow
    )
    
    # Evidence components
    static_signals: StaticSignals = Field(
        description="Signals extracted from static code analysis"
    )
    
    runtime_signals: Optional[RuntimeSignals] = Field(
        default=None,
        description="Signals captured from runtime behavior testing"
    )
    
    # Metadata
    metadata: EvidenceMetadata = Field(
        description="Collection context and quality metrics",
        default_factory=lambda: EvidenceMetadata()
    )
    
    # Schema version for evolution
    schema_version: str = Field(
        default="1.0.0",
        description="Evidence schema version",
        pattern=r"^\d+\.\d+\.\d+$"
    )
```

#### JSON Schema Example

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "EvidencePack",
  "type": "object",
  "required": ["feature_name", "repo", "static_signals"],
  "properties": {
    "feature_name": {
      "type": "string",
      "pattern": "^[a-zA-Z][a-zA-Z0-9_-]*$",
      "minLength": 1,
      "maxLength": 100,
      "description": "Unique feature identifier"
    },
    "repo": {
      "type": "string", 
      "minLength": 1,
      "maxLength": 500,
      "description": "Repository path or identifier"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "Evidence collection timestamp"
    },
    "static_signals": {
      "$ref": "#/definitions/StaticSignals"
    },
    "runtime_signals": {
      "anyOf": [
        {"$ref": "#/definitions/RuntimeSignals"},
        {"type": "null"}
      ]
    },
    "metadata": {
      "$ref": "#/definitions/EvidenceMetadata"
    },
    "schema_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "default": "1.0.0"
    }
  }
}
```

### StaticSignals Model

Structured representation of static code analysis results.

```python
from typing import List, Optional, Union, Any
from enum import Enum

class GeoBranchingSignal(BaseModel):
    """Geographic branching logic detected in code"""
    file: str = Field(description="Source file path")
    line: int = Field(ge=1, description="Line number")
    countries: List[str] = Field(
        description="ISO 3166-1 alpha-2 country codes",
        min_length=1
    )
    condition: str = Field(description="Branching condition logic")
    message: Optional[str] = Field(default=None, description="Additional context")

class AgeCheckSignal(BaseModel):
    """Age verification or checking logic detected"""
    file: str
    line: int = Field(ge=1)
    lib: Optional[str] = Field(default=None, description="Library used")
    method: Optional[str] = Field(default=None, description="Method/function name")
    threshold: Optional[int] = Field(default=None, ge=0, le=150, description="Age threshold")
    verification_type: Optional[str] = Field(
        default=None,
        description="Type of verification: collection, validation, enforcement"
    )

class DataResidencySignal(BaseModel):
    """Data residency or localization requirements"""
    file: str
    line: int = Field(ge=1)
    regions: List[str] = Field(description="Regions/jurisdictions mentioned")
    data_types: List[str] = Field(description="Types of data affected")
    mechanism: str = Field(description="Implementation mechanism")

class ReportingClientSignal(BaseModel):
    """External reporting client integration"""
    client_name: str = Field(description="Reporting service name")
    file: str
    line: int = Field(ge=1)
    api_endpoints: List[str] = Field(default_factory=list)
    trigger_conditions: List[str] = Field(default_factory=list)

class FeatureFlagSignal(BaseModel):
    """Feature flag or configuration flag"""
    name: str = Field(description="Flag name/identifier")
    file: str
    line: int = Field(ge=1)
    default_value: Optional[Union[bool, str, int]] = Field(default=None)
    description: Optional[str] = Field(default=None)

class StaticSignals(BaseModel):
    """Collection of all static analysis signals"""
    
    # Geographic compliance signals
    geo_branching: List[GeoBranchingSignal] = Field(
        default_factory=list,
        description="Geographic branching logic found in code"
    )
    
    # Age-related compliance signals  
    age_checks: List[AgeCheckSignal] = Field(
        default_factory=list,
        description="Age verification/checking implementations"
    )
    
    # Data handling signals
    data_residency: List[DataResidencySignal] = Field(
        default_factory=list,
        description="Data residency and localization controls"
    )
    
    # External integrations
    reporting_clients: List[ReportingClientSignal] = Field(
        default_factory=list,
        description="External reporting service integrations"
    )
    
    # System configuration
    reco_system: bool = Field(
        default=False,
        description="Recommendation/algorithmic system detected"
    )
    
    pf_controls: bool = Field(
        default=False,
        description="Parental/family controls detected"
    )
    
    # Feature flags and configuration
    flags: List[FeatureFlagSignal] = Field(
        default_factory=list,
        description="Feature flags and configuration switches"
    )
    
    # Semantic tags
    tags: List[str] = Field(
        default_factory=list,
        description="Semantic tags for feature categorization",
        max_length=50
    )
```

### RuntimeSignals Model

Runtime behavior evidence collected through browser automation.

```python
class PersonaTestResult(BaseModel):
    """Results from testing a single persona"""
    persona: Dict[str, Any] = Field(description="Persona configuration used")
    
    blocked_actions: List[str] = Field(
        default_factory=list,
        description="User actions that were blocked or restricted"
    )
    
    ui_states: List[str] = Field(
        default_factory=list,
        description="UI states observed (modals, warnings, etc.)"
    )
    
    flag_resolutions: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Feature flag values resolved for this persona"
    )
    
    network: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Network requests captured during testing"
    )
    
    errors: List[str] = Field(
        default_factory=list,
        description="Errors encountered during testing"
    )
    
    success: bool = Field(description="Whether testing completed successfully")
    duration_seconds: float = Field(ge=0, description="Test execution time")

class RuntimeSignals(BaseModel):
    """Collection of runtime behavior signals"""
    
    personas_tested: List[PersonaTestResult] = Field(
        description="Results from each persona tested"
    )
    
    summary: Dict[str, Any] = Field(
        description="Aggregate statistics and insights"
    )
    
    test_url: str = Field(description="Base URL used for testing")
    browser_info: Dict[str, str] = Field(description="Browser version info")
    test_timestamp: datetime = Field(default_factory=datetime.utcnow)
```

### RulesResult Model

Compliance rules evaluation results.

```python
class RuleEvaluation(BaseModel):
    """Single rule evaluation result"""
    
    rule_name: str = Field(description="Human-readable rule name")
    regulation_id: str = Field(description="Regulation/standard identifier")  
    verdict: str = Field(
        description="Compliance verdict",
        regex="^(COMPLIANT|NON_COMPLIANT|REQUIRES_REVIEW|NOT_APPLICABLE)$"
    )
    confidence: float = Field(
        ge=0.0, 
        le=1.0, 
        description="Confidence in verdict (0.0-1.0)"
    )
    reasoning: str = Field(description="Human-readable explanation")
    evidence_refs: List[str] = Field(
        description="References to supporting evidence"
    )
    priority: str = Field(
        description="Issue priority level",
        regex="^(LOW|MEDIUM|HIGH|CRITICAL)$"
    )

class ComplianceRecommendation(BaseModel):
    """Actionable compliance recommendation"""
    
    priority: str = Field(regex="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    action: str = Field(description="Recommended action")
    regulation: str = Field(description="Related regulation")
    effort_estimate: str = Field(description="Implementation effort estimate")
    evidence_gap: str = Field(description="What evidence is missing/insufficient")
    implementation_notes: Optional[str] = Field(default=None)

class RulesResult(BaseModel):
    """Complete rules evaluation results"""
    
    feature_name: str = Field(description="Feature that was evaluated")
    evaluation_timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    overall_verdict: str = Field(
        description="Overall compliance verdict across all rules",
        regex="^(COMPLIANT|NON_COMPLIANT|REQUIRES_REVIEW|NOT_APPLICABLE)$"
    )
    confidence_score: float = Field(
        ge=0.0, 
        le=1.0,
        description="Overall confidence score"
    )
    risk_level: str = Field(
        description="Overall risk assessment",
        regex="^(LOW|MEDIUM|HIGH|CRITICAL)$"
    )
    
    rule_results: List[RuleEvaluation] = Field(
        description="Individual rule evaluation results"
    )
    
    recommendations: List[ComplianceRecommendation] = Field(
        description="Prioritized recommendations for compliance"
    )
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional evaluation metadata"
    )
```

### LLMAnalysis Model

AI-generated analysis and explanations.

```python
class LLMCompliantArea(BaseModel):
    """Area where compliance is achieved"""
    regulation: str = Field(description="Regulation name")
    reasoning: str = Field(description="Why this area is compliant")

class LLMNonCompliantArea(BaseModel):
    """Area where compliance is not achieved"""
    regulation: str = Field(description="Regulation name")
    reasoning: str = Field(description="Why this area is non-compliant")
    risk_level: str = Field(regex="^(LOW|MEDIUM|HIGH|CRITICAL)$")

class LLMRequiresReviewArea(BaseModel):
    """Area requiring manual review"""
    regulation: str = Field(description="Regulation name")
    reasoning: str = Field(description="Why review is needed")
    risk_level: str = Field(regex="^(LOW|MEDIUM|HIGH|CRITICAL)$")

class LLMRecommendation(BaseModel):
    """AI-generated recommendation"""
    
    priority: str = Field(regex="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    title: str = Field(description="Recommendation title")
    description: str = Field(description="Detailed recommendation")
    effort_estimate: str = Field(description="Implementation effort")
    business_impact: str = Field(description="Business impact description")
    technical_approach: Optional[str] = Field(
        default=None,
        description="Suggested technical implementation"
    )

class LLMDetailedAnalysis(BaseModel):
    """Detailed compliance analysis breakdown"""
    
    compliant_areas: List[LLMCompliantArea] = Field(default_factory=list)
    non_compliant_areas: List[LLMNonCompliantArea] = Field(default_factory=list)
    requires_review: List[LLMRequiresReviewArea] = Field(default_factory=list)

class ConfidenceAssessment(BaseModel):
    """AI confidence in its own analysis"""
    
    overall_confidence: float = Field(
        ge=0.0, 
        le=1.0,
        description="Overall confidence in analysis"
    )
    explanation_quality: str = Field(
        description="Quality assessment of explanations",
        regex="^(LOW|MEDIUM|HIGH)$"
    )
    recommendation_actionability: str = Field(
        description="How actionable the recommendations are", 
        regex="^(LOW|MEDIUM|HIGH)$"
    )
    regulatory_accuracy: str = Field(
        description="Confidence in regulatory interpretation",
        regex="^(UNVERIFIED|PARTIAL|VERIFIED)$"
    )

class LLMAnalysis(BaseModel):
    """Complete LLM analysis results"""
    
    feature_name: str = Field(description="Feature analyzed")
    analysis_timestamp: datetime = Field(default_factory=datetime.utcnow)
    model_used: str = Field(description="LLM model identifier")
    
    # Analysis content
    executive_summary: str = Field(description="High-level summary")
    detailed_analysis: LLMDetailedAnalysis = Field(
        description="Detailed breakdown by compliance area"
    )
    key_risks: List[str] = Field(description="Key risks identified")
    recommendations: List[LLMRecommendation] = Field(
        description="AI-generated recommendations"
    )
    
    # Meta-analysis
    confidence_assessment: ConfidenceAssessment = Field(
        description="AI's confidence in its own analysis"
    )
```

## 📥 Input Schemas

### Personas Configuration

```python
class GeolocationConfig(BaseModel):
    """Geographic coordinates for location simulation"""
    latitude: float = Field(ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(ge=-180, le=180, description="Longitude coordinate")

class PersonaConfig(BaseModel):
    """Single persona configuration for runtime testing"""
    
    id: str = Field(
        description="Unique persona identifier", 
        pattern=r"^[a-z][a-z0-9_]*$"
    )
    country: str = Field(
        description="ISO 3166-1 alpha-2 country code",
        pattern=r"^[A-Z]{2}$"
    )
    state: Optional[str] = Field(
        default=None,
        description="State/province code for countries with subdivisions"
    )
    age: int = Field(ge=0, le=150, description="User age in years")
    language: str = Field(
        description="IETF language tag (e.g., en-US, de-DE)",
        pattern=r"^[a-z]{2}-[A-Z]{2}$"
    )
    timezone: str = Field(
        description="IANA timezone identifier"
    )
    
    # Testing configuration
    test_scenarios: List[str] = Field(
        description="Test scenarios to run with this persona"
    )
    
    # Optional geographic simulation
    geo_location: Optional[GeolocationConfig] = Field(
        default=None,
        description="Simulated geographic location"
    )
    
    # Compliance-specific flags
    gdpr_mode: bool = Field(default=False, description="GDPR-specific testing")
    coppa_minor: bool = Field(default=False, description="COPPA minor classification")

class PersonasConfig(BaseModel):
    """Complete personas configuration file"""
    
    version: str = Field(default="1.0", description="Configuration version")
    personas: List[PersonaConfig] = Field(description="List of personas")
    
    # Global test configuration
    default_timeout: int = Field(
        default=30,
        ge=5,
        le=300,
        description="Default timeout per persona (seconds)"
    )
    
    # Validation
    @field_validator('personas')
    @classmethod
    def validate_unique_ids(cls, v):
        ids = [p.id for p in v]
        if len(ids) != len(set(ids)):
            raise ValueError("Persona IDs must be unique")
        return v
```

### Rules Configuration

```python
from typing import Any, Dict

class ConfidenceFactors(BaseModel):
    """Factors that contribute to rule confidence calculation"""
    
    # Factor weights (must sum to 1.0)
    geo_specificity: float = Field(
        ge=0.0, le=1.0, 
        description="Weight for geographic implementation specificity"
    )
    age_verification: float = Field(
        ge=0.0, le=1.0,
        description="Weight for age verification implementation quality" 
    )
    implementation_quality: float = Field(
        ge=0.0, le=1.0,
        description="Weight for overall implementation robustness"
    )
    
    @field_validator('*')
    @classmethod
    def validate_sum_to_one(cls, v, info):
        # Validate after all fields are set
        if info.field_name == 'implementation_quality':
            # Check sum when processing last field
            total = getattr(info.data, 'geo_specificity', 0) + \
                   getattr(info.data, 'age_verification', 0) + v
            if abs(total - 1.0) > 0.001:  # Allow small floating point error
                raise ValueError("Confidence factors must sum to 1.0")
        return v

class ComplianceRule(BaseModel):
    """Single compliance rule definition"""
    
    name: str = Field(description="Human-readable rule name")
    regulation_id: str = Field(
        description="Unique regulation identifier",
        pattern=r"^[a-z][a-z0-9_]*$"
    )
    description: str = Field(description="Rule description")
    jurisdiction: str = Field(
        description="Applicable jurisdiction (e.g., US-UT, EU, global)"
    )
    
    # JSON Logic rule definition
    logic: Dict[str, Any] = Field(
        description="JSON Logic rule expression"
    )
    
    # Confidence calculation
    confidence_factors: ConfidenceFactors = Field(
        description="Factors affecting confidence calculation"
    )
    
    priority: str = Field(
        description="Rule priority level",
        regex="^(LOW|MEDIUM|HIGH|CRITICAL)$",
        default="MEDIUM"
    )
    
    # Metadata
    version: str = Field(
        default="1.0.0",
        pattern=r"^\d+\.\d+\.\d+$",
        description="Rule version"
    )
    last_updated: datetime = Field(
        default_factory=datetime.utcnow,
        description="Rule last update timestamp"
    )

class RulesConfig(BaseModel):
    """Complete rules configuration"""
    
    version: str = Field(default="1.0", description="Rules schema version")
    rules: List[ComplianceRule] = Field(description="List of compliance rules")
    
    # Global rule settings
    default_confidence_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Default confidence threshold for positive verdicts"
    )
    
    @field_validator('rules')
    @classmethod
    def validate_unique_regulation_ids(cls, v):
        ids = [rule.regulation_id for rule in v]
        if len(ids) != len(set(ids)):
            raise ValueError("Regulation IDs must be unique")
        return v
```

## 📤 Output Schemas  

### CSV Export Schema

The CSV output follows a standardized schema for data analysis and reporting tools:

```python
class CSVExportRow(BaseModel):
    """Single row in CSV export"""
    
    # Feature identification
    feature_name: str = Field(description="Feature identifier")
    analysis_timestamp: datetime = Field(description="Analysis timestamp")
    
    # Overall assessment
    overall_verdict: str = Field(
        description="COMPLIANT|NON_COMPLIANT|REQUIRES_REVIEW|NOT_APPLICABLE"
    )
    confidence_score: float = Field(
        ge=0.0, le=1.0, 
        description="Overall confidence (0.0-1.0)"
    )
    risk_level: str = Field(
        description="LOW|MEDIUM|HIGH|CRITICAL"
    )
    
    # Regulatory coverage
    regulations_tested: int = Field(ge=0, description="Number of regulations tested")
    compliant_regulations: int = Field(ge=0, description="Regulations passed")
    non_compliant_regulations: int = Field(ge=0, description="Regulations failed")
    
    # Evidence metrics
    evidence_quality_score: float = Field(
        ge=0.0, le=1.0,
        description="Evidence completeness (0.0-1.0)"
    )
    static_signals_count: int = Field(ge=0, description="Static signals found")
    runtime_signals_count: int = Field(ge=0, description="Runtime signals found")
    
    # Recommendations
    high_priority_recommendations: int = Field(
        ge=0, 
        description="Number of high-priority recommendations"
    )
    estimated_effort_weeks: int = Field(
        ge=0,
        description="Estimated remediation effort in weeks"
    )
    primary_recommendation: str = Field(description="Top recommendation summary")
    
    # Regulatory details
    regulatory_references: str = Field(
        description="Comma-separated regulation IDs"
    )
```

### HTML Report Schema

HTML reports use a structured template system:

```python
class HTMLReportData(BaseModel):
    """Data structure for HTML report generation"""
    
    # Report metadata
    report_title: str = Field(description="Report title")
    generation_timestamp: datetime = Field(description="Report generation time")
    cds_version: str = Field(description="CDS version used")
    
    # Executive summary
    executive_summary: Dict[str, Any] = Field(
        description="High-level metrics and charts data"
    )
    
    # Feature analysis
    features: List[Dict[str, Any]] = Field(
        description="Per-feature analysis results"
    )
    
    # Regulatory matrix
    regulatory_matrix: Dict[str, Dict[str, str]] = Field(
        description="Feature vs regulation compliance matrix"
    )
    
    # Recommendations
    recommendations: List[Dict[str, Any]] = Field(
        description="Prioritized recommendations with details"
    )
    
    # Technical details
    technical_details: Dict[str, Any] = Field(
        description="Evidence details, confidence analysis, etc."
    )
    
    # Styling and branding
    branding: Dict[str, str] = Field(
        default_factory=dict,
        description="Organization branding configuration"
    )
```

## 🔧 Configuration Schemas

### Main Configuration Schema

```python
class LoggingConfig(BaseModel):
    """Logging configuration"""
    level: str = Field(
        default="INFO",
        regex="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"
    )
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file: Optional[str] = Field(default=None, description="Log file path")
    max_file_size: str = Field(default="10MB", description="Log rotation size")
    backup_count: int = Field(default=5, ge=1, le=20)

class OutputConfig(BaseModel):
    """Output configuration"""
    directory: str = Field(default="artifacts", description="Base output directory")
    formats: List[str] = Field(
        default=["csv", "html"],
        description="Default export formats"
    )
    retention_days: int = Field(default=30, ge=1, le=365)

class ScannerConfig(BaseModel):
    """Scanner configuration"""
    timeout: int = Field(default=300, ge=30, le=3600, description="Timeout in seconds")
    parallel_jobs: int = Field(default=4, ge=1, le=16)
    rules_directories: List[str] = Field(default_factory=list)
    exclude_patterns: List[str] = Field(
        default=["node_modules", "*.git", "build", "dist"]
    )

class RuntimeConfig(BaseModel):
    """Runtime probing configuration"""
    enabled: bool = Field(default=True)
    timeout: int = Field(default=30, ge=5, le=300)
    retry_attempts: int = Field(default=3, ge=1, le=5)
    default_personas: str = Field(default="data/personas/default.json")
    browsers: List[str] = Field(default=["chromium", "firefox"])
    viewport: str = Field(default="1920x1080", pattern=r"^\d+x\d+$")

class LLMConfig(BaseModel):
    """LLM integration configuration"""
    provider: str = Field(
        default="gemini",
        regex="^(gemini|openai|anthropic)$"
    )
    model: str = Field(default="gemini-1.5-pro")
    temperature: float = Field(default=0.1, ge=0.0, le=1.0)
    max_tokens: int = Field(default=4096, ge=100, le=32768)
    cache_enabled: bool = Field(default=True)
    rate_limit: int = Field(default=10, ge=1, le=100, description="Requests per minute")

class CDSConfig(BaseModel):
    """Main CDS configuration"""
    
    version: str = Field(default="1.0", description="Config version")
    
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    scanner: ScannerConfig = Field(default_factory=ScannerConfig)
    runtime: RuntimeConfig = Field(default_factory=RuntimeConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    
    # Organization settings
    organization: Dict[str, Any] = Field(
        default_factory=dict,
        description="Organization-specific settings"
    )
```

## ✅ Validation Rules

### Field Validation

CDS implements comprehensive validation using Pydantic validators:

```python
from pydantic import field_validator, model_validator
import re
from typing import List

class ValidationMixin:
    """Common validation methods"""
    
    @field_validator('feature_name')
    @classmethod
    def validate_feature_name(cls, v: str) -> str:
        """Feature names must be valid identifiers"""
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', v):
            raise ValueError(
                'Feature name must start with letter and contain only letters, '
                'numbers, underscores, and hyphens'
            )
        return v
    
    @field_validator('country')
    @classmethod  
    def validate_country_code(cls, v: str) -> str:
        """Validate ISO 3166-1 alpha-2 country codes"""
        valid_codes = [
            'AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AS', 'AT',
            'AU', 'AW', 'AX', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI',
            'BJ', 'BL', 'BM', 'BN', 'BO', 'BQ', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY',
            'BZ', 'CA', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN',
            'CO', 'CR', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM',
            'DO', 'DZ', 'EC', 'EE', 'EG', 'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK',
            'FM', 'FO', 'FR', 'GA', 'GB', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GL',
            'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK', 'HM',
            'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IR',
            'IS', 'IT', 'JE', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN',
            'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS',
            'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MK',
            'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW',
            'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP',
            'NR', 'NU', 'NZ', 'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM',
            'PN', 'PR', 'PS', 'PT', 'PW', 'PY', 'QA', 'RE', 'RO', 'RS', 'RU', 'RW',
            'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM',
            'SN', 'SO', 'SR', 'SS', 'ST', 'SV', 'SX', 'SY', 'SZ', 'TC', 'TD', 'TF',
            'TG', 'TH', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW',
            'TZ', 'UA', 'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI',
            'VN', 'VU', 'WF', 'WS', 'YE', 'YT', 'ZA', 'ZM', 'ZW'
        ]
        if v not in valid_codes:
            raise ValueError(f'Invalid country code: {v}')
        return v
    
    @field_validator('timezone')
    @classmethod
    def validate_timezone(cls, v: str) -> str:
        """Validate IANA timezone identifiers"""
        import zoneinfo
        try:
            zoneinfo.ZoneInfo(v)
        except zoneinfo.ZoneInfoNotFoundError:
            raise ValueError(f'Invalid timezone: {v}')
        return v

class ModelValidationMixin:
    """Model-level validation methods"""
    
    @model_validator(mode='after')
    def validate_persona_age_compliance_flags(self):
        """Ensure compliance flags match age"""
        if hasattr(self, 'age') and hasattr(self, 'coppa_minor'):
            if self.age < 13 and not self.coppa_minor:
                raise ValueError('Users under 13 should have coppa_minor=True')
            if self.age >= 13 and self.coppa_minor:
                raise ValueError('Users 13+ should have coppa_minor=False')
        return self
```

### Cross-Field Validation

```python
class EvidenceValidation:
    """Evidence-specific validation logic"""
    
    @model_validator(mode='after')  
    def validate_evidence_consistency(self):
        """Ensure evidence components are consistent"""
        
        # If runtime signals present, should have static signals
        if self.runtime_signals and not self.static_signals:
            raise ValueError("Runtime signals require corresponding static signals")
            
        # Feature name should match across components
        if self.runtime_signals:
            if self.runtime_signals.feature_name != self.feature_name:
                raise ValueError("Feature name mismatch between evidence components")
                
        return self
    
    @field_validator('static_signals')
    @classmethod
    def validate_static_signals_quality(cls, v: StaticSignals) -> StaticSignals:
        """Validate static signals quality"""
        
        total_signals = (
            len(v.geo_branching) + 
            len(v.age_checks) + 
            len(v.data_residency) + 
            len(v.reporting_clients) +
            len(v.flags)
        )
        
        if total_signals == 0:
            raise ValueError("Evidence must contain at least one signal")
            
        return v

class RulesValidation:
    """Rules validation logic"""
    
    @field_validator('logic')
    @classmethod
    def validate_json_logic(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Validate JSON Logic syntax"""
        import jsonlogic
        
        try:
            # Test compilation
            jsonlogic.jsonLogic(v, {})
        except Exception as e:
            raise ValueError(f"Invalid JSON Logic: {e}")
            
        return v
```

## 🔄 Schema Evolution

CDS supports schema evolution through versioning:

```python
class SchemaVersion(BaseModel):
    """Schema version tracking"""
    
    major: int = Field(ge=0, description="Major version (breaking changes)")
    minor: int = Field(ge=0, description="Minor version (new features)")  
    patch: int = Field(ge=0, description="Patch version (fixes)")
    
    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"
    
    @classmethod
    def from_string(cls, version_str: str) -> 'SchemaVersion':
        """Parse version from string"""
        parts = version_str.split('.')
        if len(parts) != 3:
            raise ValueError("Version must be in format MAJOR.MINOR.PATCH")
        return cls(
            major=int(parts[0]),
            minor=int(parts[1]), 
            patch=int(parts[2])
        )

# Schema migration handling
class SchemaMigration:
    """Handle schema migrations"""
    
    @staticmethod
    def migrate_evidence_pack(data: Dict[str, Any], from_version: str, to_version: str) -> Dict[str, Any]:
        """Migrate evidence pack between schema versions"""
        
        from_v = SchemaVersion.from_string(from_version)
        to_v = SchemaVersion.from_string(to_version)
        
        if from_v.major < to_v.major:
            # Major version changes require manual migration
            raise ValueError(f"Cannot automatically migrate from {from_version} to {to_version}")
            
        # Handle minor version migrations
        if from_v.minor < to_v.minor:
            data = cls._migrate_minor_version(data, from_v, to_v)
            
        return data
    
    @staticmethod
    def _migrate_minor_version(data: Dict[str, Any], from_v: SchemaVersion, to_v: SchemaVersion) -> Dict[str, Any]:
        """Handle minor version migrations"""
        
        # Example: 1.0.x -> 1.1.x added metadata field
        if from_v.minor == 0 and to_v.minor >= 1:
            if 'metadata' not in data:
                data['metadata'] = {
                    'collection_method': 'automated',
                    'quality_score': 0.8,
                    'completeness': True
                }
                
        return data
```

## 📚 Examples

### Complete Evidence Pack Example

```json
{
  "feature_name": "user_registration",
  "repo": "./social-media-app",
  "timestamp": "2024-12-15T10:30:00Z",
  "static_signals": {
    "geo_branching": [
      {
        "file": "auth/geo_logic.py",
        "line": 45,
        "countries": ["US", "CA", "EU"],
        "condition": "if user.country in ['US-UT', 'US-TX']",
        "message": "State-specific age verification routing"
      }
    ],
    "age_checks": [
      {
        "file": "auth/registration.py",
        "line": 123,
        "lib": "dateutil",
        "method": "calculate_age_from_birthdate",
        "threshold": 13,
        "verification_type": "collection"
      },
      {
        "file": "auth/verification.py", 
        "line": 67,
        "lib": "document_verify",
        "method": "verify_government_id",
        "threshold": 18,
        "verification_type": "validation"
      }
    ],
    "data_residency": [
      {
        "file": "database/config.py",
        "line": 34,
        "regions": ["EU", "US"],
        "data_types": ["user_profiles", "messages"],
        "mechanism": "database_routing"
      }
    ],
    "reporting_clients": [
      {
        "client_name": "ncmec_client",
        "file": "safety/reporting.py",
        "line": 89,
        "api_endpoints": ["https://api.ncmec.org/report"],
        "trigger_conditions": ["child_exploitation_detected"]
      }
    ],
    "reco_system": true,
    "pf_controls": true,
    "flags": [
      {
        "name": "utah_age_verification_enabled",
        "file": "config/feature_flags.py",
        "line": 45,
        "default_value": true,
        "description": "Enable Utah-specific age verification flow"
      },
      {
        "name": "eu_gdpr_consent_v2",
        "file": "config/feature_flags.py",
        "line": 52,
        "default_value": false,
        "description": "Enable GDPR Article 8 consent flow v2"
      }
    ],
    "tags": ["authentication", "age_sensitive", "geo_aware", "social_features"]
  },
  "runtime_signals": {
    "personas_tested": [
      {
        "persona": {
          "id": "us_utah_minor",
          "country": "US",
          "state": "UT", 
          "age": 16,
          "language": "en-US",
          "coppa_minor": false
        },
        "blocked_actions": [
          "direct_messaging_strangers",
          "location_sharing",
          "friend_recommendations_auto_accept"
        ],
        "ui_states": [
          "age_verification_modal_shown",
          "parental_consent_required_banner",
          "restricted_features_notification"
        ],
        "flag_resolutions": [
          {"name": "utah_age_verification_enabled", "value": true},
          {"name": "social_features_restricted", "value": true},
          {"name": "parental_controls_required", "value": true}
        ],
        "network": [
          {
            "host": "api.myapp.com",
            "method": "POST", 
            "path": "/auth/verify-age",
            "status": 200,
            "headers": {"X-User-State": "UT"}
          },
          {
            "host": "compliance.myapp.com",
            "method": "POST",
            "path": "/utah/minor-registration",  
            "status": 201
          }
        ],
        "errors": [],
        "success": true,
        "duration_seconds": 45.2
      },
      {
        "persona": {
          "id": "eu_germany_adult",
          "country": "DE",
          "age": 25,
          "language": "de-DE",
          "gdpr_mode": true
        },
        "blocked_actions": [],
        "ui_states": [
          "gdpr_consent_modal",
          "data_processing_explanation",
          "legitimate_interests_notice"
        ],
        "flag_resolutions": [
          {"name": "eu_gdpr_consent_v2", "value": true},
          {"name": "data_minimization_enabled", "value": true}
        ],
        "network": [
          {
            "host": "eu.myapp.com",
            "method": "POST",
            "path": "/gdpr/consent",
            "status": 200
          }
        ],
        "errors": [],
        "success": true,
        "duration_seconds": 38.1
      }
    ],
    "summary": {
      "total_personas": 5,
      "successful_probes": 5,
      "failed_probes": 0,
      "unique_behaviors": 3,
      "compliance_patterns": ["age_gating", "geo_routing", "consent_collection"]
    },
    "test_url": "https://staging.myapp.com",
    "browser_info": {
      "name": "chromium",
      "version": "120.0.6099.62"
    },
    "test_timestamp": "2024-12-15T10:35:00Z"
  },
  "metadata": {
    "collection_method": "automated_pipeline",
    "scanner_version": "1.0.0", 
    "quality_score": 0.95,
    "completeness": true,
    "collection_duration_seconds": 125.3,
    "warnings": []
  },
  "schema_version": "1.0.0"
}
```

### Pipeline Output JSON Example

```json
{
  "pipeline_results": {
    "execution_id": "pipeline_20241215_103000",
    "timestamp": "2024-12-15T10:30:00Z",
    "features_analyzed": [
      {
        "feature_name": "user_registration",
        "overall_verdict": "REQUIRES_REVIEW",
        "confidence_score": 0.87,
        "risk_level": "MEDIUM",
        "regulations": {
          "utah_social_media_2024": {
            "verdict": "NON_COMPLIANT",
            "confidence": 0.92,
            "priority": "HIGH"
          },
          "coppa_child_protection": {
            "verdict": "COMPLIANT", 
            "confidence": 0.89,
            "priority": "MEDIUM"
          },
          "gdpr_article8": {
            "verdict": "REQUIRES_REVIEW",
            "confidence": 0.73,
            "priority": "MEDIUM"
          }
        },
        "recommendations": [
          {
            "priority": "HIGH",
            "title": "Implement Utah Age Verification",
            "effort_estimate": "2-3 weeks"
          },
          {
            "priority": "MEDIUM",
            "title": "Enhance GDPR Consent Flow", 
            "effort_estimate": "1 week"
          }
        ]
      }
    ],
    "summary": {
      "total_features": 3,
      "compliant_features": 1, 
      "non_compliant_features": 1,
      "requires_review_features": 1,
      "overall_risk": "MEDIUM",
      "total_recommendations": 8,
      "high_priority_recommendations": 3,
      "estimated_total_effort": "6-8 weeks"
    }
  }
}
```

---

**📝 Last Updated**: December 2024  
**🔄 Schema Version**: 1.0.0  
**📖 Related Docs**: [CLI Reference](cli-reference.md) | [User Manual](../guides/user-manual.md) | [System Architecture](../architecture/system-overview.md)

This reference provides complete schema documentation for all CDS data structures. For implementation examples and usage patterns, see our [guides](../guides/) and [architecture documentation](../architecture/).
