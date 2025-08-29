#!/usr/bin/env python3
"""
CDS Pipeline Demo

This script demonstrates the complete compliance detection pipeline
with sample data and generates a final report.
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


def create_demo_dataset():
    """Create a demo dataset for pipeline testing"""
    print("📋 Creating demo dataset...")
    
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
            "feature_id": "data_export_service",
            "repo_path": "./sample_repo",
            "description": "User data export for GDPR portability rights"
        }
    ]
    
    dataset_path = Path("./data/demo_dataset.csv")
    df = pd.DataFrame(dataset_data)
    df.to_csv(dataset_path, index=False)
    
    print(f"✅ Created demo dataset with {len(dataset_data)} features: {dataset_path}")
    return dataset_path


def prepare_demo_evidence():
    """Create evidence files for demo features"""
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
    """Run the complete demo pipeline"""
    print("🚀 CDS Compliance Detection System - Pipeline Demo")
    print("=" * 70)
    
    try:
        # Step 1: Create demo dataset
        dataset_path = create_demo_dataset()
        
        # Step 2: Prepare evidence files
        prepare_demo_evidence()
        
        # Step 3: Run the pipeline
        print(f"\n🔄 Running compliance detection pipeline...")
        
        output_csv = Path("./artifacts/demo_results.csv")
        report_html = Path("./artifacts/demo_report.html")
        
        results = run_pipeline(dataset_path, output_csv, report_html)
        
        print(f"\n" + "=" * 70)
        print(f"🎉 Pipeline Demo Completed Successfully!")
        
        print(f"\n📊 Results Summary:")
        print(f"   • Total Features: {results['total_features']}")
        print(f"   • Successfully Processed: {results['processed_count']}")
        print(f"   • Errors: {results['error_count']}")
        
        print(f"\n📄 Generated Files:")
        print(f"   • CSV Results: {output_csv}")
        print(f"   • HTML Report: {report_html}")
        print(f"   • Evidence Files: ./artifacts/evidence/")
        
        print(f"\n🌟 Next Steps:")
        print(f"   1. Open {report_html} in your browser to view the compliance report")
        print(f"   2. Review {output_csv} for programmatic access to results")
        print(f"   3. Check ./artifacts/evidence/ for detailed evidence files")
        
        print(f"\n💡 To view the HTML report:")
        print(f"   Open: file:///{Path(report_html).resolve()}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
