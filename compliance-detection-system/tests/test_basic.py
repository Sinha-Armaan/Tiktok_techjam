"""
Basic tests to validate CDS setup and functionality
"""

import pytest
import json
from pathlib import Path
from cds.evidence.models import EvidencePack, StaticSignals, GeoSignal
from cds.scanner.main import StaticAnalysisEngine
from cds.rules.main import ComplianceRulesEngine
from cds.llm.main import LLMAnalysisEngine


def test_evidence_pack_creation():
    """Test basic evidence pack functionality"""
    evidence = EvidencePack(feature_id="test_feature")
    
    # Add static signals
    static_signals = StaticSignals()
    static_signals.geo_branching.append(GeoSignal(
        file="test.py",
        line=10,
        countries=["US", "CA"]
    ))
    
    evidence.add_static_signals(static_signals)
    
    assert evidence.feature_id == "test_feature"
    assert len(evidence.static.geo_branching) == 1
    assert evidence.static.geo_branching[0].countries == ["US", "CA"]


def test_static_analysis_engine():
    """Test static analysis engine initialization"""
    engine = StaticAnalysisEngine()
    assert engine.semgrep is not None
    assert engine.treesitter is not None


def test_rules_engine_initialization():
    """Test compliance rules engine setup"""
    engine = ComplianceRulesEngine()
    assert len(engine.rules) > 0
    
    # Check for key rules
    rule_ids = set(engine.rules.keys())
    expected_rules = {
        "UT_MINORS_CURFEW",
        "NCMEC_REPORTING", 
        "DSA_TRANSPARENCY",
        "GDPR_DATA_PROCESSING"
    }
    
    assert expected_rules.issubset(rule_ids)


def test_llm_analysis_engine():
    """Test LLM analysis engine initialization"""
    engine = LLMAnalysisEngine()
    assert engine.gemini_client is not None
    assert engine.policy_manager is not None
    
    # Test policy snippets loading
    assert len(engine.policy_manager.snippets) > 0


def test_sample_repo_exists():
    """Test that sample repo with compliance patterns exists"""
    sample_repo = Path(__file__).parent.parent / "sample_repo"
    assert sample_repo.exists()
    
    # Check for key files
    expected_files = [
        "user_registration.py",
        "content_recommendation.py", 
        "privacy_settings.py"
    ]
    
    for filename in expected_files:
        assert (sample_repo / filename).exists()


def test_configuration_files():
    """Test that all required configuration files exist"""
    base_path = Path(__file__).parent.parent
    
    required_files = [
        "data/rules/semgrep.yml",
        "data/rules/compliance_rules.json",
        "data/policy_snippets.json",
        "data/sample_dataset.csv"
    ]
    
    for filepath in required_files:
        full_path = base_path / filepath
        assert full_path.exists(), f"Missing required file: {filepath}"


def test_semgrep_rules_format():
    """Test that semgrep rules are properly formatted"""
    rules_file = Path(__file__).parent.parent / "data/rules/semgrep.yml"
    
    # Basic YAML loading test
    import yaml
    with open(rules_file, 'r') as f:
        rules_data = yaml.safe_load(f)
    
    assert "rules" in rules_data
    assert len(rules_data["rules"]) > 0
    
    # Check first rule structure
    first_rule = rules_data["rules"][0]
    required_fields = ["id", "pattern-either", "message", "languages"]
    
    for field in required_fields:
        assert field in first_rule, f"Missing field {field} in semgrep rule"


def test_json_rules_format():
    """Test that JSON Logic rules are properly formatted"""
    rules_file = Path(__file__).parent.parent / "data/rules/compliance_rules.json"
    
    with open(rules_file, 'r') as f:
        rules_data = json.load(f)
    
    assert "rules" in rules_data
    assert len(rules_data["rules"]) > 0
    
    # Check first rule structure
    first_rule = rules_data["rules"][0]
    required_fields = ["id", "name", "logic", "regulations", "severity"]
    
    for field in required_fields:
        assert field in first_rule, f"Missing field {field} in compliance rule"


def test_policy_snippets_format():
    """Test that policy snippets are properly formatted"""
    snippets_file = Path(__file__).parent.parent / "data/policy_snippets.json"
    
    with open(snippets_file, 'r') as f:
        snippets_data = json.load(f)
    
    assert isinstance(snippets_data, list)
    assert len(snippets_data) > 0
    
    # Check first snippet structure
    first_snippet = snippets_data[0]
    required_fields = ["regulation_id", "title", "content", "jurisdiction"]
    
    for field in required_fields:
        assert field in first_snippet, f"Missing field {field} in policy snippet"


if __name__ == "__main__":
    pytest.main([__file__])
