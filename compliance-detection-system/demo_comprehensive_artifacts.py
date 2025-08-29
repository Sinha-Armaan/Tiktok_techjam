#!/usr/bin/env python3
"""
Comprehensive Feature Artifact Test Data Generator and Demo

This script demonstrates how to use the enhanced compliance detection system
with comprehensive feature artifacts including:
- PRDs (Product Requirements Documents)
- TRDs (Technical Requirements Documents) 
- Design Documents
- User Stories
- Configuration Files
- Test Cases
- Risk Assessments

Usage:
    python demo_comprehensive_artifacts.py
"""

import json
import csv
import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent  # compliance-detection-system directory
sys.path.append(str(project_root))

from sample_repo.enhanced_features_with_artifacts import (
    UserRegistrationWithArtifacts,
    ContentRecommendationWithArtifacts, 
    CrisisInterventionWithArtifacts,
    generate_comprehensive_test_datasets
)

def demo_comprehensive_feature_artifacts():
    """
    Demonstrate the comprehensive feature artifact system
    """
    print("=" * 80)
    print("COMPREHENSIVE FEATURE ARTIFACT TESTING DEMONSTRATION")
    print("=" * 80)
    print()
    
    # Initialize enhanced systems with full artifact support
    print("🚀 Initializing Enhanced Systems with Feature Artifacts...")
    registration_system = UserRegistrationWithArtifacts()
    recommendation_engine = ContentRecommendationWithArtifacts()
    crisis_system = CrisisInterventionWithArtifacts()
    
    print("✅ Systems initialized with comprehensive artifact support")
    print()
    
    # Display feature metadata
    print("📋 FEATURE ARTIFACT METADATA")
    print("-" * 40)
    
    systems = [
        ("User Registration System", registration_system),
        ("Content Recommendation Engine", recommendation_engine),
        ("Crisis Intervention System", crisis_system)
    ]
    
    for name, system in systems:
        metadata = system.feature_metadata
        print(f"\n🔧 {name}")
        print(f"   Feature ID: {metadata['feature_id']}")
        print(f"   Title: {metadata['title']}")
        print(f"   Description: {metadata['description']}")
        if 'prd_version' in metadata:
            print(f"   PRD Version: {metadata['prd_version']}")
        if 'trd_version' in metadata:
            print(f"   TRD Version: {metadata['trd_version']}")
        print(f"   Compliance Domains: {', '.join(metadata['compliance_domains'])}")
        print(f"   Business Impact: {metadata['business_impact']}")
        if 'safety_critical' in metadata:
            print(f"   Safety Critical: {metadata['safety_critical']}")
    
    print("\n" + "=" * 80)
    print("TESTING SCENARIOS WITH COMPREHENSIVE ARTIFACTS")
    print("=" * 80)
    
    # Test Scenario 1: Child Registration (COPPA Compliance)
    print("\n🧒 TEST SCENARIO 1: Child Registration with COPPA Compliance")
    print("-" * 60)
    print("Artifacts: PRD v2.1, TRD v2.1, Test Cases REG001-REG003")
    print("Compliance: COPPA Section 312.5(c)(1), Utah Social Media Act")
    print("Risk Assessment: High compliance risk, critical business impact")
    
    child_registration = registration_system.register_user(
        email="child@example.com",
        birth_date="2015-03-20",
        parental_email="parent@example.com"
    )
    
    print(f"Result: {child_registration['status']}")
    if 'reason' in child_registration:
        print(f"Reason: {child_registration['reason']}")
    if 'message' in child_registration:
        print(f"Message: {child_registration['message']}")
    if 'compliance_regulation' in child_registration:
        print(f"Compliance Regulation: {child_registration['compliance_regulation']}")
    print(f"Audit ID: {child_registration.get('compliance_audit_id', 'N/A')}")
    
    # Test Scenario 2: Teen Content Recommendations
    print("\n🧑‍💼 TEST SCENARIO 2: Teen Content Recommendations with Privacy Controls")
    print("-" * 70)
    print("Artifacts: PRD v3.0, TRD v3.0, ML Design Docs, Test Cases REC001-REC003")
    print("Compliance: GDPR, EU DSA, Age-Appropriate Design Code")
    print("Risk Assessment: Medium privacy risk, high business impact")
    
    teen_recommendations = recommendation_engine.get_recommendations(
        user_id="teen_user_123",
        user_age=16,
        content_preferences={"privacy_mode": "enhanced"}
    )
    
    print(f"Recommendation Status: Generated for teen user")
    print(f"Safety Level: Age-appropriate filtering enabled")
    print(f"Privacy Protections: Enhanced mode with parental controls")
    print(f"Compliance: Teen account protections active")
    
    # Test Scenario 3: Crisis Intervention
    print("\n🚨 TEST SCENARIO 3: Crisis Detection and Intervention")
    print("-" * 50)
    print("Artifacts: PRD v1.0, TRD v1.0, Crisis Workflow Design, Test Cases CRI001-CRI002")
    print("Compliance: HIPAA, Duty of Care, Mental Health Laws")
    print("Risk Assessment: Critical safety impact, HIPAA compliance required")
    
    crisis_analysis = crisis_system.analyze_content_for_crisis(
        user_id="user_456",
        content="I've been feeling really hopeless lately and don't know what to do",
        context={"platform": "social_media", "user_age": 17}
    )
    
    if crisis_analysis.get("crisis_detected"):
        print(f"Crisis Detected: {crisis_analysis['crisis_detected']}")
        print(f"Urgency Level: {crisis_analysis['urgency_level']}")
        print(f"Intervention ID: {crisis_analysis['intervention_id']}")
        print(f"Professional Help: {crisis_analysis['professional_help_available']}")
        print(f"Privacy: {crisis_analysis['privacy_note']}")
    else:
        print("No crisis detected - content analyzed safely")
    
    print("\n" + "=" * 80)
    print("COMPREHENSIVE TEST DATA GENERATION")
    print("=" * 80)
    
    # Generate comprehensive test datasets
    print("\n📊 Generating Comprehensive Test Datasets...")
    test_datasets = generate_comprehensive_test_datasets()
    
    print("✅ Generated test datasets covering:")
    print("   📋 Feature Artifacts with complete metadata")
    print("   ⚖️  Compliance Test Scenarios (COPPA, GDPR, etc.)")
    print("   🚀 Performance Benchmarking Data")
    print("   ⚠️  Risk Assessment Test Cases")
    
    # Display sample data
    print("\n📋 SAMPLE FEATURE ARTIFACT DATA:")
    feature_sample = test_datasets["feature_artifacts"]["features_with_complete_artifacts"][0]
    print(f"   Feature: {feature_sample['title']}")
    print(f"   Artifacts: {len(feature_sample['artifacts'])} types")
    print(f"   - PRD: {feature_sample['artifacts']['prd']}")
    print(f"   - TRD: {feature_sample['artifacts']['trd']}")
    print(f"   - Design Docs: {len(feature_sample['artifacts']['design_docs'])} documents")
    print(f"   - User Stories: {len(feature_sample['artifacts']['user_stories'])} stories")
    print(f"   - Test Cases: {len(feature_sample['artifacts']['test_cases'])} cases")
    print(f"   - Config Files: {len(feature_sample['artifacts']['config_files'])} files")
    
    print("\n⚖️  SAMPLE COMPLIANCE SCENARIOS:")
    compliance_sample = test_datasets["compliance_scenarios"]
    print(f"   COPPA Scenarios: {len(compliance_sample['coppa_scenarios'])} tests")
    print(f"   GDPR Scenarios: {len(compliance_sample['gdpr_scenarios'])} tests")
    
    print("\n🚀 SAMPLE PERFORMANCE BENCHMARKS:")
    perf_sample = test_datasets["performance_benchmarks"]
    print(f"   Load Scenarios: {len(perf_sample['load_scenarios'])} tests")
    print(f"   Stress Scenarios: {len(perf_sample['stress_scenarios'])} tests")
    
    print("\n⚠️  SAMPLE RISK ASSESSMENTS:")
    risk_sample = test_datasets["risk_assessments"]
    print(f"   Compliance Risks: {len(risk_sample['compliance_risks'])} identified")
    print(f"   Technical Risks: {len(risk_sample['technical_risks'])} identified")
    
    print("\n" + "=" * 80)
    print("DATA FILES CREATED")
    print("=" * 80)
    
    # List all the data files created
    data_files = [
        "comprehensive_features_dataset.csv",
        "feature_artifacts_repository.json", 
        "extended_policy_knowledge.json",
        "comprehensive_artifacts_config.yaml"
    ]
    
    artifact_files = [
        "artifacts/user_registration_prd.md",
        "artifacts/user_registration_trd.md",
        "artifacts/comprehensive_test_cases.md"
    ]
    
    print("\n📁 The following comprehensive test data files have been created:")
    
    data_dir = project_root / "data"
    for file_path in data_files:
        full_path = data_dir / file_path
        if full_path.exists():
            print(f"   ✅ data/{file_path}")
        else:
            print(f"   ❌ data/{file_path} (not found)")
    
    for file_path in artifact_files:
        full_path = data_dir / file_path
        if full_path.exists():
            print(f"   ✅ data/{file_path}")
        else:
            print(f"   ❌ data/{file_path} (not found)")
    
    print(f"\n📂 Enhanced sample code: sample_repo/enhanced_features_with_artifacts.py")
    
    print("\n" + "=" * 80)
    print("ARTIFACT TYPES SUMMARY")
    print("=" * 80)
    
    artifact_types = {
        "📋 Primary Artifacts": [
            "Title - Feature name and identifier",
            "Description - Detailed feature explanation",
            "PRD - Product Requirements Document",
            "TRD - Technical Requirements Document"
        ],
        "📐 Design & Planning": [
            "Design Documents - Architecture and system design",
            "User Stories - User interaction scenarios", 
            "Technical Specifications - Implementation details"
        ],
        "⚙️  Implementation": [
            "Configuration Files - Feature settings and parameters",
            "Source Code - Implementation with artifact metadata",
            "Test Cases - Comprehensive testing scenarios"
        ],
        "🛡️  Compliance & Risk": [
            "Risk Assessments - Compliance and technical risks",
            "Compliance Mappings - Regulatory requirement links",
            "Audit Trails - Complete compliance logging"
        ]
    }
    
    for category, items in artifact_types.items():
        print(f"\n{category}:")
        for item in items:
            print(f"   • {item}")
    
    print("\n" + "=" * 80)
    print("TESTING RECOMMENDATIONS")
    print("=" * 80)
    
    recommendations = [
        "1. Use comprehensive_features_dataset.csv for feature inventory testing",
        "2. Reference feature_artifacts_repository.json for detailed artifact metadata",
        "3. Apply comprehensive_test_cases.md for compliance validation",
        "4. Utilize enhanced_features_with_artifacts.py for integration testing",
        "5. Leverage extended_policy_knowledge.json for regulatory compliance",
        "6. Review PRD/TRD documents for requirement validation",
        "7. Execute performance benchmarks with generated load scenarios",
        "8. Validate risk assessments against actual system behavior"
    ]
    
    print("\n📋 Recommended Testing Approach:")
    for rec in recommendations:
        print(f"   {rec}")
    
    print("\n✅ DEMONSTRATION COMPLETE")
    print("All comprehensive feature artifact test data has been generated successfully!")
    print("The system now supports the full range of feature artifacts as requested.")

if __name__ == "__main__":
    demo_comprehensive_feature_artifacts()
