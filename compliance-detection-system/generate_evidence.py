#!/usr/bin/env python3
"""
Evidence Generator for Dataset Variations

This script generates evidence files from the artifacts created by the dataset generators,
allowing the compliance detection pipeline to analyze the intentional issues we introduced.
"""

import json
import os
from pathlib import Path
import pandas as pd
from datetime import datetime


def create_evidence_from_artifacts(dataset_variation):
    """Create evidence files from dataset variation artifacts"""
    print(f"🔍 Creating evidence files for {dataset_variation}...")
    
    # Define paths
    variation_path = Path(f"dataset_variations/{dataset_variation}")
    data_path = variation_path / "data"
    artifacts_path = variation_path / "artifacts"
    evidence_dir = Path("artifacts/evidence")
    
    # Ensure evidence directory exists
    evidence_dir.mkdir(parents=True, exist_ok=True)
    
    # Load the feature dataset
    feature_files = {
        "original_comprehensive_focused": "comprehensive_features_dataset.csv",
        "enterprise_security_focused": "enterprise_security_features.csv", 
        "global_expansion_focused": "global_expansion_features.csv"
    }
    
    if dataset_variation not in feature_files:
        print(f"❌ Unknown dataset variation: {dataset_variation}")
        return
        
    feature_file = data_path / feature_files[dataset_variation]
    if not feature_file.exists():
        print(f"❌ Feature file not found: {feature_file}")
        return
        
    # Load features
    df = pd.read_csv(feature_file)
    print(f"📋 Loaded {len(df)} features from {dataset_variation}")
    
    # Create evidence files for each feature
    evidence_files_created = []
    
    for _, feature in df.iterrows():
        feature_id = feature['feature_id']
        
        # Look for corresponding PRD and TRD files
        prd_file = artifacts_path / f"{feature_id}_{dataset_variation.split('_')[-2]}_prd.md"
        trd_file = artifacts_path / f"{feature_id}_{dataset_variation.split('_')[-2]}_trd.md"
        code_file = None
        
        # Look for code files in different directories
        for code_dir in ["enhanced_code", "security_code", "global_code"]:
            code_path = variation_path / code_dir
            if code_path.exists():
                for code_file_path in code_path.glob(f"{feature_id}_*"):
                    code_file = code_file_path
                    break
                if code_file:
                    break
        
        # Create evidence JSON
        evidence = {
            "feature_id": feature_id,
            "feature_name": feature.get('title', feature_id),
            "created_at": datetime.now().isoformat(),
            "dataset_variation": dataset_variation,
            "artifacts": {
                "prd_available": prd_file.exists() if prd_file else False,
                "trd_available": trd_file.exists() if trd_file else False, 
                "code_available": code_file.exists() if code_file else False
            },
            "static_analysis": {
                "files_analyzed": [],
                "compliance_signals": {
                    "age_verification_signals": 0,
                    "geographic_branching_signals": 0,
                    "data_residency_signals": 0,
                    "consent_management_signals": 0
                },
                "security_issues": {
                    "hardcoded_secrets": 0,
                    "sql_injection_risks": 0,
                    "missing_validation": 0,
                    "insecure_connections": 0
                }
            },
            "rules_engine": {
                "requires_geo_logic": False,
                "confidence_score": 0.0,
                "matched_rules": [],
                "compliance_domains": feature.get('compliance_domains', '').split(',') if pd.notna(feature.get('compliance_domains')) else []
            }
        }
        
        # Add file contents if they exist (truncated for analysis)
        if prd_file and prd_file.exists():
            try:
                with open(prd_file, 'r', encoding='utf-8') as f:
                    prd_content = f.read()[:5000]  # First 5000 chars
                    evidence['artifacts']['prd_content_sample'] = prd_content
                    evidence['static_analysis']['files_analyzed'].append(str(prd_file))
                    
                    # Look for intentional compliance issues in PRD
                    compliance_keywords = ['missing', 'inadequate', 'insufficient', 'unclear', 'gap', 'oversight', 'weakness']
                    for keyword in compliance_keywords:
                        if keyword.lower() in prd_content.lower():
                            evidence['static_analysis']['compliance_signals']['potential_issues'] = evidence['static_analysis']['compliance_signals'].get('potential_issues', 0) + 1
                            
            except Exception as e:
                print(f"⚠️  Error reading PRD {prd_file}: {e}")
        
        if trd_file and trd_file.exists():
            try:
                with open(trd_file, 'r', encoding='utf-8') as f:
                    trd_content = f.read()[:5000]  # First 5000 chars  
                    evidence['artifacts']['trd_content_sample'] = trd_content
                    evidence['static_analysis']['files_analyzed'].append(str(trd_file))
                    
                    # Look for security issues in TRD
                    security_keywords = ['hardcoded', 'sql injection', 'missing validation', 'insecure', 'weak encryption', 'plaintext']
                    for keyword in security_keywords:
                        if keyword.lower() in trd_content.lower():
                            evidence['static_analysis']['security_issues']['potential_vulnerabilities'] = evidence['static_analysis']['security_issues'].get('potential_vulnerabilities', 0) + 1
                            
            except Exception as e:
                print(f"⚠️  Error reading TRD {trd_file}: {e}")
                
        if code_file and code_file.exists():
            try:
                with open(code_file, 'r', encoding='utf-8') as f:
                    code_content = f.read()[:10000]  # First 10000 chars
                    evidence['artifacts']['code_content_sample'] = code_content
                    evidence['static_analysis']['files_analyzed'].append(str(code_file))
                    
                    # Look for intentional code vulnerabilities
                    vuln_patterns = {
                        'hardcoded_secrets': ['hardcoded', 'api_key', 'password', 'secret'],
                        'sql_injection_risks': ['sql injection', 'raw sql', 'unsanitized'],
                        'missing_validation': ['missing validation', 'no validation', 'unvalidated'],
                        'insecure_connections': ['http://', 'insecure connection', 'no encryption']
                    }
                    
                    for vuln_type, patterns in vuln_patterns.items():
                        for pattern in patterns:
                            if pattern.lower() in code_content.lower():
                                evidence['static_analysis']['security_issues'][vuln_type] += 1
                                
            except Exception as e:
                print(f"⚠️  Error reading code {code_file}: {e}")
        
        # Save evidence file
        evidence_file = evidence_dir / f"{feature_id}.json"
        with open(evidence_file, 'w', encoding='utf-8') as f:
            json.dump(evidence, f, indent=2)
            
        evidence_files_created.append(evidence_file)
        print(f"✅ Created evidence: {evidence_file}")
    
    print(f"🎯 Created {len(evidence_files_created)} evidence files for {dataset_variation}")
    return evidence_files_created


def main():
    """Generate evidence files for all dataset variations"""
    variations = [
        "original_comprehensive_focused",
        "enterprise_security_focused", 
        "global_expansion_focused"
    ]
    
    print("🔍 Evidence Generator for Dataset Variations")
    print("=" * 60)
    
    total_evidence_files = []
    
    for variation in variations:
        try:
            evidence_files = create_evidence_from_artifacts(variation)
            total_evidence_files.extend(evidence_files)
            print()
        except Exception as e:
            print(f"❌ Error processing {variation}: {e}")
            print()
    
    print(f"🎉 Generated {len(total_evidence_files)} total evidence files")
    print("🚀 Ready to run compliance detection pipeline!")


if __name__ == "__main__":
    main()
