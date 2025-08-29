#!/usr/bin/env python3
"""
Real Repository Analysis Script
"""

import pandas as pd
from pathlib import Path

def create_real_repo_dataset(repo_path, features):
    """Create dataset for real repository analysis"""
    
    dataset_data = []
    for feature in features:
        dataset_data.append({
            "feature_id": feature,
            "repository_path": str(repo_path),
            "description": f"Analysis of {feature} feature",
            "priority": "high"
        })
    
    df = pd.DataFrame(dataset_data)
    dataset_path = Path("./data/real_repo_dataset.csv")
    df.to_csv(dataset_path, index=False)
    
    print(f"✅ Created dataset with {len(features)} features: {dataset_path}")
    return dataset_path

if __name__ == "__main__":
    # Example: Analyze features in your own repository
    repo_path = input("Enter repository path (or . for current): ").strip() or "."
    
    print("\nSuggested features to analyze:")
    print("- user_authentication")
    print("- payment_processing") 
    print("- content_moderation")
    print("- data_collection")
    print("- user_registration")
    print("- messaging_system")
    
    features_input = input("\nEnter features to analyze (comma-separated): ")
    features = [f.strip() for f in features_input.split(",") if f.strip()]
    
    if not features:
        features = ["user_authentication", "data_collection"]
        print(f"Using default features: {features}")
    
    # Create dataset
    dataset_path = create_real_repo_dataset(repo_path, features)
    
    # Run pipeline
    print(f"\n🚀 To run the full analysis, execute:")
    print(f"cds pipeline -d {dataset_path}")
