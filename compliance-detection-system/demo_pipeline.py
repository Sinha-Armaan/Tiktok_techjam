#!/usr/bin/env python3
"""
CDS Pipeline Demo with Comprehensive Feature Artifacts

This script demonstrates the complete compliance detection pipeline
with comprehensive feature artifacts including PRDs, TRDs, design docs,
user stories, config files, test cases, and risk assessments.
"""

import json
import sys
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the cds module to Python path
sys.path.insert(0, str(Path(__file__).parent))

from cds.evidence.pipeline import run_pipeline


def load_comprehensive_dataset():
    """Load the comprehensive feature artifacts dataset"""
    print("📋 Loading comprehensive feature artifacts dataset...")
    
    dataset_path = Path("./data/comprehensive_features_dataset.csv")
    if not dataset_path.exists():
        print("❌ Comprehensive dataset not found. Creating basic demo dataset...")
        return create_basic_demo_dataset()
    
    # Load comprehensive dataset
    df = pd.read_csv(dataset_path)
    
    print(f"✅ Loaded {len(df)} features with comprehensive artifacts")
    print(f"   📋 Features with PRDs: {df['prd_available'].sum()}")
    print(f"   📋 Features with TRDs: {df['trd_available'].sum()}")
    print(f"   📋 Features with Design Docs: {df['design_docs'].sum()}")
    print(f"   📋 Features with User Stories: {df['user_stories'].sum()}")
    print(f"   📋 Features with Test Cases: {df['test_cases'].sum()}")
    print(f"   📋 Features with Risk Assessments: {df['risk_assessment'].count()}")
    
    return dataset_path


def create_basic_demo_dataset():
    """Create a basic demo dataset as fallback"""
    print("📋 Creating basic demo dataset...")
    
    # Create sample dataset with our test features
    dataset_data = [
        {
            "feature_id": "user_registration_system",
            "repo_path": "./sample_repo",
            "description": "User registration with age verification and geographic restrictions"
        },
        {
            "feature_id": "content_recommendation_engine", 
            "repo_path": "./sample_repo",
            "description": "Content recommendation system with CSAM detection and NCMEC reporting"
        },
        {
            "feature_id": "privacy_settings_manager",
            "repo_path": "./sample_repo", 
            "description": "Privacy settings with GDPR and CCPA compliance features"
        },
        {
            "feature_id": "messaging_system",
            "repo_path": "./sample_repo",
            "description": "Direct messaging with minor protection features"
        },
        {
            "feature_id": "age_verification_gate",
            "repo_path": "./sample_repo",
            "description": "Age gate implementation for COPPA compliance"
        }
    ]
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(dataset_data)
    dataset_path = Path("./data/demo_dataset.csv")
    dataset_path.parent.mkdir(exist_ok=True)
    df.to_csv(dataset_path, index=False)
    
    print(f"✅ Created basic demo dataset with {len(df)} features")
    print(f"   💾 Saved to: {dataset_path}")
    
    return dataset_path


def load_comprehensive_artifacts():
    """Load comprehensive feature artifacts for enhanced pipeline testing"""
    print("\n🔍 Loading comprehensive feature artifacts...")
    
    artifacts_path = Path("./data/feature_artifacts_repository.json")
    if artifacts_path.exists():
        with open(artifacts_path, 'r') as f:
            artifacts = json.load(f)
        
        print(f"✅ Loaded comprehensive artifacts repository (v{artifacts['version']})")
        print(f"   📋 Features with detailed artifacts: {len(artifacts['features'])}")
        
        for feature in artifacts['features']:
            feature_id = feature['feature_id']
            artifacts_available = feature['artifacts']
            
            print(f"\n   🔧 {feature['title']} ({feature_id}):")
            if 'prd' in artifacts_available:
                print(f"      📋 PRD: {artifacts_available['prd']['title']}")
            if 'trd' in artifacts_available:
                print(f"      🔧 TRD: {artifacts_available['trd']['title']}")
            if 'design_docs' in artifacts_available:
                print(f"      📐 Design Docs: {len(artifacts_available['design_docs'])} documents")
            if 'user_stories' in artifacts_available:
                print(f"      👤 User Stories: {len(artifacts_available['user_stories'])} stories")
            if 'test_cases' in artifacts_available:
                print(f"      🧪 Test Cases: {len(artifacts_available['test_cases'])} tests")
            if 'risk_assessment' in artifacts_available:
                compliance_risks = len(artifacts_available['risk_assessment'].get('compliance_risks', []))
                technical_risks = len(artifacts_available['risk_assessment'].get('technical_risks', []))
                print(f"      ⚠️  Risk Assessment: {compliance_risks} compliance + {technical_risks} technical risks")
        
        return artifacts
    else:
        print("⚠️  Comprehensive artifacts not available, using basic demo data")
        return None


def prepare_comprehensive_evidence():
    """Prepare evidence files with comprehensive artifact support"""
    print("\n📁 Preparing comprehensive evidence files...")
    
    # Create evidence directory
    evidence_dir = Path("./artifacts/evidence")
    evidence_dir.mkdir(parents=True, exist_ok=True)
    
    # Load extended policy knowledge
    policy_path = Path("./data/extended_policy_knowledge.json")
    if policy_path.exists():
        with open(policy_path, 'r') as f:
            extended_policies = json.load(f)
        
        # Save enhanced policy evidence
        enhanced_policy_evidence = {
            "version": extended_policies["version"],
            "regulation_count": len(extended_policies["regulations"]),
            "compliance_frameworks": len(extended_policies.get("compliance_frameworks", [])),
            "regulations": {}
        }
        
        for regulation in extended_policies["regulations"]:
            reg_id = regulation["regulation_id"]
            enhanced_policy_evidence["regulations"][reg_id] = {
                "title": regulation["title"],
                "jurisdiction": regulation["jurisdiction"],
                "effective_date": regulation["effective_date"],
                "key_requirements_count": len(regulation["key_requirements"]),
                "compliance_mechanisms_count": len(regulation["compliance_mechanisms"]),
                "penalties": regulation["penalties"]
            }
        
        evidence_file = evidence_dir / "comprehensive_policy_evidence.json"
        with open(evidence_file, 'w') as f:
            json.dump(enhanced_policy_evidence, f, indent=2)
        
        print(f"✅ Enhanced policy evidence: {evidence_file}")
        print(f"   📋 Regulations covered: {len(extended_policies['regulations'])}")
        print(f"   🌍 Jurisdictions: {', '.join(set(r['jurisdiction'] for r in extended_policies['regulations']))}")
    
    # Load comprehensive test cases
    test_cases_path = Path("./data/artifacts/comprehensive_test_cases.md")
    if test_cases_path.exists():
        print(f"✅ Comprehensive test cases available: {test_cases_path}")
        
        # Create test evidence summary
        test_evidence = {
            "test_categories": [
                "User Registration (COPPA compliance)",
                "Content Recommendation (Privacy compliance)",
                "Crisis Intervention (Safety compliance)",
                "Age Verification (Multi-regulation compliance)",
                "Privacy and Data Protection (GDPR compliance)",
                "Performance and Reliability"
            ],
            "compliance_domains": [
                "COPPA", "GDPR", "Utah Social Media Act", "EU DSA", 
                "CCPA", "HIPAA", "NCMEC Reporting"
            ],
            "test_case_file": str(test_cases_path)
        }
        
        evidence_file = evidence_dir / "comprehensive_test_evidence.json" 
        with open(evidence_file, 'w') as f:
            json.dump(test_evidence, f, indent=2)
        
        print(f"✅ Test case evidence: {evidence_file}")
    
    print(f"📁 Evidence preparation complete")


def create_demo_dataset():
    """Create enhanced demo dataset with comprehensive artifacts"""
    print("📋 Creating enhanced demo dataset with comprehensive artifacts...")
    
    # Try to load comprehensive dataset first
    comprehensive_path = Path("./data/comprehensive_features_dataset.csv")
    if comprehensive_path.exists():
        print(f"✅ Using comprehensive features dataset: {comprehensive_path}")
        return comprehensive_path
    
    # Fallback to basic dataset
    return create_basic_demo_dataset()


def prepare_demo_evidence():
    """Create evidence files for demo features with comprehensive artifact support"""
    print("\n📁 Preparing evidence files with comprehensive artifact support...")
    
    # Use the comprehensive evidence preparation if available
    try:
        prepare_comprehensive_evidence()
        return
    except Exception as e:
        print(f"⚠️  Using basic evidence preparation: {e}")
    
    # Fallback to basic evidence preparation
    print("\n📁 Preparing demo evidence files...")
    
    evidence_dir = Path("./artifacts/evidence")
    evidence_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample evidence data for each feature
    demo_evidence = {
        "user_registration_system": {
            "feature_id": "user_registration_system",
            "signals": {
                "static": {
                    "geo_branching": [
                        {"file": "user_registration.py", "line": 15, "countries": ["US", "CA", "GB", "FR", "DE"]}
                    ],
                    "age_checks": [
                        {"file": "user_registration.py", "line": 32, "lib": "age_gate"}
                    ],
                    "data_residency": [
                        {"file": "user_registration.py", "line": 95, "region": "us-east"},
                        {"file": "user_registration.py", "line": 96, "region": "eu-west"}
                    ],
                    "reporting_clients": [],
                    "reco_system": False,
                    "pf_controls": True,
                    "flags": [{"name": "FEATURE_FLAG_COMPLIANCE_UTAH_MINORS"}],
                    "tags": ["user_data", "age_verification"]
                }
            },
            "attachments": [],
            "metadata": {"repo": "./sample_repo", "scan_timestamp": "2025-08-28T10:00:00Z"}
        },
        
        "content_recommendation_engine": {
            "feature_id": "content_recommendation_engine", 
            "signals": {
                "static": {
                    "geo_branching": [
                        {"file": "content_recommendation.py", "line": 85, "countries": ["US", "CA", "GB", "FR", "DE"]}
                    ],
                    "age_checks": [],
                    "data_residency": [],
                    "reporting_clients": ["NCMEC"],
                    "reco_system": True,
                    "pf_controls": False,
                    "flags": [{"name": "FEATURE_FLAG_COMPLIANCE_CSAM_DETECTION"}],
                    "tags": ["content_moderation", "csam_detection", "recommendation"]
                }
            },
            "attachments": [],
            "metadata": {"repo": "./sample_repo", "scan_timestamp": "2025-08-28T10:00:00Z"}
        },
        
        "privacy_settings_manager": {
            "feature_id": "privacy_settings_manager",
            "signals": {
                "static": {
                    "geo_branching": [
                        {"file": "privacy_settings.py", "line": 45, "countries": ["EU", "GB", "CA"]}
                    ],
                    "age_checks": [],
                    "data_residency": [
                        {"file": "privacy_settings.py", "line": 110, "region": "eu-west"}
                    ],
                    "reporting_clients": [],
                    "reco_system": False,
                    "pf_controls": True,
                    "flags": [],
                    "tags": ["user_data", "privacy", "gdpr"]
                }
            },
            "attachments": [],
            "metadata": {"repo": "./sample_repo", "scan_timestamp": "2025-08-28T10:00:00Z"}
        }
    }
    
    # Create evidence files
    for feature_id, evidence_data in demo_evidence.items():
        evidence_file = evidence_dir / f"{feature_id}.json"
        with open(evidence_file, 'w') as f:
            json.dump(evidence_data, f, indent=2)
        print(f"   • Created evidence for {feature_id}")
    
    print(f"✅ Created {len(demo_evidence)} evidence files")


def main():
    """Run the complete demo pipeline with comprehensive feature artifacts"""
    print("🚀 CDS Compliance Detection System - Enhanced Pipeline Demo")
    print("=" * 80)
    print("🎯 Features: Comprehensive artifacts including PRDs, TRDs, design docs, user stories, test cases, and risk assessments")
    print("=" * 80)
    
    try:
        # Step 1: Load comprehensive artifacts
        artifacts = load_comprehensive_artifacts()
        
        # Step 2: Create enhanced demo dataset
        dataset_path = create_demo_dataset()
        
        # Step 3: Prepare comprehensive evidence files
        prepare_comprehensive_evidence()
        
        # Step 4: Display comprehensive dataset info
        if dataset_path.name == "comprehensive_features_dataset.csv":
            df = pd.read_csv(dataset_path)
            print(f"\n📊 Comprehensive Dataset Loaded:")
            print(f"   📋 Total Features: {len(df)}")
            print(f"   📋 Features with PRDs: {df['prd_available'].sum()}")
            print(f"   📋 Features with TRDs: {df['trd_available'].sum()}")
            print(f"   📋 Features with Design Docs: {df['design_docs'].sum()}")
            print(f"   📋 Features with User Stories: {df['user_stories'].sum()}")
            print(f"   📋 Features with Test Cases: {df['test_cases'].sum()}")
            print(f"   ⚖️  Compliance Domains: {', '.join(df['compliance_domains'].str.split(',').explode().unique())}")
            print(f"   🎯 Business Impact Distribution:")
            print(f"      • Critical: {(df['business_impact'] == 'critical').sum()}")
            print(f"      • High: {(df['business_impact'] == 'high').sum()}")
            print(f"      • Medium: {(df['business_impact'] == 'medium').sum()}")
        
        # Step 5: Run the enhanced pipeline
        print(f"\n🔄 Running enhanced compliance detection pipeline...")
        
        output_csv = Path("./artifacts/comprehensive_demo_results.csv")
        report_html = Path("./artifacts/comprehensive_demo_report.html")
        
        results = run_pipeline(dataset_path, output_csv, report_html)
        
        print(f"\n" + "=" * 80)
        print(f"🎉 Enhanced Pipeline Demo Completed Successfully!")
        
        print(f"\n📊 Results Summary:")
        print(f"   • Total Features: {results['total_features']}")
        print(f"   • Successfully Processed: {results['processed_count']}")
        print(f"   • Errors: {results['error_count']}")
        
        if artifacts:
            print(f"   📋 Features with Comprehensive Artifacts: {len(artifacts['features'])}")
            print(f"   🔧 Artifact Types Analyzed: PRDs, TRDs, Design Docs, User Stories, Test Cases, Risk Assessments")
        
        print(f"\n📄 Generated Files:")
        print(f"   • Enhanced CSV Results: {output_csv}")
        print(f"   • Comprehensive HTML Report: {report_html}")
        print(f"   • Evidence Files: ./artifacts/evidence/")
        if Path("./artifacts/evidence/comprehensive_policy_evidence.json").exists():
            print(f"   • Extended Policy Evidence: ./artifacts/evidence/comprehensive_policy_evidence.json")
        if Path("./artifacts/evidence/comprehensive_test_evidence.json").exists():
            print(f"   • Comprehensive Test Evidence: ./artifacts/evidence/comprehensive_test_evidence.json")
        
        print(f"\n🌟 Enhanced Features Available:")
        print(f"   1. 📋 20 features with complete artifact metadata")
        print(f"   2. ⚖️  8+ major compliance regulations covered")
        print(f"   3. 📋 Complete PRD/TRD examples with technical specifications")
        print(f"   4. 🧪 15+ comprehensive test scenarios")
        print(f"   5. ⚠️  Detailed risk assessments (compliance + technical)")
        print(f"   6. 🔧 Working implementation examples with artifact annotations")
        
        print(f"\n💡 To view the enhanced HTML report:")
        print(f"   Open: file:///{Path(report_html).resolve()}")
        
        print(f"\n🚀 Next Steps:")
        print(f"   1. Review {report_html} for comprehensive compliance analysis")
        print(f"   2. Examine {output_csv} for programmatic access to enhanced results")
        print(f"   3. Explore ./data/artifacts/ for PRD/TRD examples")
        print(f"   4. Run python demo_comprehensive_artifacts.py for artifact-specific demo")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Enhanced demo failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
