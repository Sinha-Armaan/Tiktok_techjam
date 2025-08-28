#!/usr/bin/env python3
"""
CDS Setup and Demo Script

This script initializes the CDS environment and runs a basic demo.
"""

import os
import sys
from pathlib import Path
import subprocess


def setup_environment():
    """Set up the CDS environment"""
    print("🚀 Setting up Compliance Detection System...")
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ required")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Create directories
    directories = [
        "artifacts/evidence",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Check if .env exists
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file from template...")
        subprocess.run(["copy" if os.name == "nt" else "cp", ".env.example", ".env"], check=True)
        print("✅ Created .env file")
    
    return True


def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install the package in development mode
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], check=True)
        print("✅ Installed CDS package")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def run_demo():
    """Run a basic demo"""
    print("\n🎯 Running CDS demo...")
    
    try:
        # Test CLI help
        result = subprocess.run([sys.executable, "-m", "cds.cli.main", "--help"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ CLI is working")
        else:
            print("❌ CLI test failed")
            return False
        
        # Try scanning the sample repo
        print("\n🔍 Running static analysis on sample repo...")
        result = subprocess.run([
            sys.executable, "-m", "cds.cli.main", "scan", 
            "--repo", "./sample_repo", 
            "--feature", "demo_feature"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Static scan completed")
            print("📄 Check ./artifacts/evidence/demo_feature.json for results")
        else:
            print("❌ Static scan failed")
            print(f"Error: {result.stderr}")
        
        # Try rules evaluation
        print("\n⚖️ Running rules evaluation...")
        result = subprocess.run([
            sys.executable, "-m", "cds.cli.main", "evaluate",
            "--feature", "demo_feature"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Rules evaluation completed")
        else:
            print("❌ Rules evaluation failed")
            print(f"Error: {result.stderr}")
        
        print("\n🎉 Demo completed!")
        print("\nNext steps:")
        print("1. Set up Google Cloud credentials in .env for LLM features")
        print("2. Run: cds pipeline --dataset ./data/sample_dataset.csv")
        print("3. Check artifacts/ directory for results")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False


def main():
    """Main setup and demo function"""
    print("=" * 60)
    print("🛠️  CDS - Compliance Detection System Setup")
    print("=" * 60)
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Run demo
    if not run_demo():
        sys.exit(1)
    
    print("\n✅ CDS setup completed successfully!")


if __name__ == "__main__":
    main()
