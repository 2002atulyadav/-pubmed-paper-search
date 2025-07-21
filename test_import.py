#!/usr/bin/env python3
"""
Quick test script to verify all imports work correctly.
"""

try:
    # Test external dependencies
    import requests
    import click
    print("✅ External dependencies (requests, click) imported successfully")
    
    # Test internal modules
    from pubmed_search import PubMedClient, PubMedPaper, PubMedCSVWriter
    print("✅ Internal modules imported successfully")
    
    # Test CLI module
    from pubmed_search.cli import main
    print("✅ CLI module imported successfully")
    
    print("\n🎉 All imports successful! The code structure is correct.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're in the right directory and dependencies are installed.")
except Exception as e:
    print(f"❌ Unexpected error: {e}")