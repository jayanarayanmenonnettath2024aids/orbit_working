#!/usr/bin/env python3
"""
Setup verification script for Opportunity Intelligence System
Checks that all components are properly configured
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} NOT FOUND: {filepath}")
        return False

def check_env_var(var_name, required=True):
    """Check if environment variable is set"""
    value = os.getenv(var_name)
    if value:
        print(f"✅ {var_name}: {'*' * 10} (set)")
        return True
    else:
        status = "❌ REQUIRED" if required else "⚠️  Optional"
        print(f"{status} {var_name}: Not set")
        return not required

def main():
    print("=" * 60)
    print("🔍 Opportunity Intelligence System - Setup Verification")
    print("=" * 60)
    print()

    all_good = True

    # Check project structure
    print("📁 Checking Project Structure...")
    print("-" * 60)
    
    structure_checks = [
        ("backend/app.py", "Backend main application"),
        ("backend/requirements.txt", "Python dependencies"),
        ("backend/.env.example", "Backend env example"),
        ("backend/services/firebase_service.py", "Firebase service"),
        ("backend/services/profile_service.py", "Profile service"),
        ("backend/services/opportunity_service.py", "Opportunity service"),
        ("backend/services/reasoning_service.py", "Reasoning service"),
        ("frontend/package.json", "Frontend dependencies"),
        ("frontend/src/App.jsx", "Frontend main app"),
        ("frontend/src/components/Dashboard.jsx", "Dashboard component"),
        ("frontend/src/components/ProfileBuilder.jsx", "Profile builder"),
        ("frontend/src/components/OpportunityExplorer.jsx", "Opportunity explorer"),
        ("README.md", "Main documentation"),
        ("ARCHITECTURE.md", "Architecture documentation"),
        ("GEMINI_PROMPTS.md", "Prompt templates"),
        ("QUICKSTART.md", "Quick start guide"),
    ]

    for filepath, description in structure_checks:
        if not check_file_exists(filepath, description):
            all_good = False

    print()

    # Check environment configuration
    print("🔧 Checking Environment Configuration...")
    print("-" * 60)
    
    # Load .env if it exists
    env_file = Path("backend/.env")
    if env_file.exists():
        print(f"✅ Found .env file: {env_file}")
        from dotenv import load_dotenv
        load_dotenv(env_file)
    else:
        print(f"⚠️  .env file not found (using environment variables)")
        print(f"   Expected location: {env_file}")
        print()

    # Check environment variables
    env_checks = [
        ("GEMINI_API_KEY", True),
        ("GOOGLE_SEARCH_API_KEY", False),
        ("GOOGLE_SEARCH_ENGINE_ID", False),
        ("FIREBASE_CONFIG_PATH", False),
    ]

    for var_name, required in env_checks:
        if not check_env_var(var_name, required):
            if required:
                all_good = False

    print()

    # Check Python dependencies
    print("🐍 Checking Python Dependencies...")
    print("-" * 60)
    
    try:
        import flask
        print(f"✅ Flask: {flask.__version__}")
    except ImportError:
        print("❌ Flask not installed")
        all_good = False

    try:
        import google.generativeai as genai
        print(f"✅ Google Generative AI SDK installed")
    except ImportError:
        print("❌ google-generativeai not installed")
        all_good = False

    try:
        import firebase_admin
        print(f"✅ Firebase Admin SDK installed")
    except ImportError:
        print("❌ firebase-admin not installed")
        all_good = False

    try:
        import PyPDF2
        print(f"✅ PyPDF2 installed")
    except ImportError:
        print("❌ PyPDF2 not installed")
        all_good = False

    print()

    # Check Node.js dependencies
    print("📦 Checking Node.js Dependencies...")
    print("-" * 60)
    
    node_modules = Path("frontend/node_modules")
    if node_modules.exists():
        print(f"✅ node_modules exists: {node_modules}")
    else:
        print(f"⚠️  node_modules not found. Run: cd frontend && npm install")
        all_good = False

    print()

    # Final summary
    print("=" * 60)
    if all_good:
        print("✅ ALL CHECKS PASSED!")
        print()
        print("🚀 Ready to run!")
        print()
        print("Start the application:")
        print("  1. Terminal 1: cd backend && python app.py")
        print("  2. Terminal 2: cd frontend && npm run dev")
        print("  3. Open: http://localhost:3000")
    else:
        print("⚠️  SOME ISSUES FOUND")
        print()
        print("Next steps:")
        print("  1. Install missing dependencies:")
        print("     Backend: cd backend && pip install -r requirements.txt")
        print("     Frontend: cd frontend && npm install")
        print("  2. Configure environment variables:")
        print("     cd backend && cp .env.example .env")
        print("     Edit .env and add your API keys")
        print("  3. Run this script again to verify")
    print("=" * 60)

    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
