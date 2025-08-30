#!/usr/bin/env python3
"""
CDS Test Script - Quick validation of core functionality

This script tests the core CDS pipeline components without requiring
external dependencies like semgrep or playwright.
"""

import json
import sys
from pathlib import Path

# Add the cds module to Python path
sys.path.insert(0, str(Path(__file__).parent))

from cds.evidence.models import (
    EvidencePack, StaticSignals, GeoSignal, AgeCheckSignal, 
    DataResidencySignal, FlagSignal, EvidenceMetadata, RulesResult
)
from cds.rules.main import ComplianceRulesEngine
from cds.llm.main import LLMAnalysisEngine


def create_test_evidence() -> EvidencePack:
    """Create test evidence with sample compliance signals"""
    print("📋 Creating test evidence...")
    
    # Create static signals
    static_signals = StaticSignals()
    
    # Add geo-branching signals
    static_signals.geo_branching = [
        GeoSignal(
            file="dataset_variations/original_comprehensive_focused/enhanced_code/user_registration_service.py",
            line=15,
            countries=["US", "CA", "GB", "FR", "DE"],
            message="Geographic country list detected"
        )
    ]
    
    # Add age verification signals
    static_signals.age_checks = [
        AgeCheckSignal(
            file="dataset_variations/original_comprehensive_focused/enhanced_code/user_registration_service.py", 
            line=32,
            lib="age_gate",
            message="Age verification import found"
        )
    ]
    
    # Add data residency signals
    static_signals.data_residency = [
        DataResidencySignal(
            file="dataset_variations/original_comprehensive_focused/enhanced_code/user_registration_service.py",
            line=95,
            region="us-east",
            message="Data region configuration"
        ),
        DataResidencySignal(
            file="dataset_variations/original_comprehensive_focused/enhanced_code/user_registration_service.py",
            line=96,
            region="eu-west",
            message="EU data region configuration"
        )
    ]
    
    # Add reporting clients
    static_signals.reporting_clients = ["NCMEC"]
    
    # Add parental controls flag
    static_signals.pf_controls = True
    
    # Add compliance feature flags
    static_signals.flags = [
        FlagSignal(name="COMPLIANCE_UTAH_MINORS"),
        FlagSignal(name="COMPLIANCE_GDPR_MODE"),
        FlagSignal(name="COMPLIANCE_COPPA_STRICT")
    ]
    
    # Add tags
    static_signals.tags = ["user_data", "age_verification", "geo_restrictions"]
    
    # Create evidence pack
    evidence = EvidencePack(
        feature_id="test_user_registration",
        metadata=EvidenceMetadata(
            repo="./dataset_variations/original_comprehensive_focused/enhanced_code",
            commit="test_commit"
        )
    )
    evidence.add_static_signals(static_signals)
    
    print(f"✅ Created evidence with {len(static_signals.geo_branching)} geo signals, "
          f"{len(static_signals.age_checks)} age signals, "
          f"{len(static_signals.data_residency)} data residency signals")
    
    return evidence


def test_rules_engine(evidence: EvidencePack) -> RulesResult:
    """Test the compliance rules engine"""
    print("\n⚖️ Testing rules engine...")
    
    engine = ComplianceRulesEngine()
    rules_result = engine.evaluate(evidence)
    
    print(f"✅ Rules evaluation complete:")
    print(f"   • Requires geo logic: {rules_result.requires_geo_logic}")
    print(f"   • Confidence score: {rules_result.confidence:.2f}")
    print(f"   • Matched rules: {rules_result.matched_rules}")
    print(f"   • Missing controls: {len(rules_result.missing_controls)} identified")
    
    return rules_result


def test_llm_analysis(evidence: EvidencePack, rules_result: RulesResult):
    """Test LLM analysis (using mock implementation)"""
    print("\n🤖 Testing LLM analysis...")
    
    engine = LLMAnalysisEngine()
    
    # Save evidence file for LLM analysis
    evidence_file = Path("./artifacts/evidence/test_user_registration.json")
    evidence_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(evidence_file, 'w') as f:
        json.dump(evidence.model_dump(), f, indent=2, default=str)
    
    # Save rules result file
    rules_file = evidence_file.parent / "test_user_registration_rules_result.json"
    with open(rules_file, 'w') as f:
        json.dump(rules_result.model_dump(), f, indent=2, default=str)
    
    # Run LLM analysis
    final_record = engine.explain_feature("test_user_registration")
    
    print(f"✅ LLM analysis complete:")
    print(f"   • Requires geo logic: {final_record.requires_geo_logic}")
    print(f"   • Severity: {final_record.severity}")
    print(f"   • Needs review: {final_record.needs_review}")
    print(f"   • Related regulations: {len(final_record.related_regulations)}")
    
    return final_record


def main():
    """Run comprehensive CDS test"""
    print("🚀 CDS Compliance Detection System - Test Suite")
    print("=" * 60)
    
    try:
        # Test 1: Create evidence
        evidence = create_test_evidence()
        
        # Test 2: Rules engine
        rules_result = test_rules_engine(evidence)
        
        # Test 3: LLM analysis
        final_record = test_llm_analysis(evidence, rules_result)
        
        print("\n" + "=" * 60)
        print("🎉 All tests completed successfully!")
        print("\n📊 Final Results:")
        print(f"   • Feature ID: {final_record.feature_id}")
        print(f"   • Compliance Required: {'YES' if final_record.requires_geo_logic else 'NO'}")
        print(f"   • Confidence: {final_record.confidence:.0%}")
        print(f"   • Severity: {final_record.severity.upper()}")
        print(f"   • Evidence Files: ./artifacts/evidence/")
        
        print(f"\n💡 Reasoning:")
        print(f"   {final_record.reasoning}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
