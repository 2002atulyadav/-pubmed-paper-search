#!/usr/bin/env python3
"""
Test script for CLI functionality without making actual API calls.
"""

import sys
from pubmed_search.cli import main
from click.testing import CliRunner

def test_cli_help():
    """Test if CLI help works."""
    print("🧪 Testing CLI help functionality...")
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    
    if result.exit_code == 0:
        print("✅ CLI help works correctly")
        print("📝 Help output preview:")
        print(result.output[:200] + "..." if len(result.output) > 200 else result.output)
    else:
        print(f"❌ CLI help failed with exit code: {result.exit_code}")
        print(f"Error: {result.output}")

def test_cli_validation():
    """Test parameter validation."""
    print("\n🧪 Testing parameter validation...")
    runner = CliRunner()
    
    # Test invalid max-results
    result = runner.invoke(main, ['test', '--max-results', '-1'])
    if "max-results must be a positive integer" in result.output:
        print("✅ Parameter validation works correctly")
    else:
        print(f"❌ Parameter validation issue: {result.output}")

if __name__ == "__main__":
    test_cli_help()
    test_cli_validation()