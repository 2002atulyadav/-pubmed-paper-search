#!/usr/bin/env python3
"""
End-to-end test script for the complete CLI functionality.
This simulates real usage scenarios.
"""

import os
import sys
import subprocess
import tempfile
import csv

def run_cli_command(args, expect_success=True):
    """Run CLI command and return result."""
    try:
        cmd = [sys.executable, "-m", "pubmed_search.cli"] + args
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if expect_success and result.returncode != 0:
            print(f"❌ Command failed: {' '.join(args)}")
            print(f"   Error: {result.stderr}")
            return None
        
        return result
    except subprocess.TimeoutExpired:
        print(f"⏰ Command timed out: {' '.join(args)}")
        return None
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return None

def test_help():
    """Test help functionality."""
    print("🧪 Testing CLI help...")
    result = run_cli_command(["--help"])
    
    if result and "PubMed" in result.stdout:
        print("✅ Help command works")
        return True
    else:
        print("❌ Help command failed")
        return False

def test_simple_query():
    """Test with a simple query that should find results."""
    print("\n🧪 Testing simple query (aspirin, max 3 results)...")
    
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as f:
        temp_file = f.name
    
    try:
        args = ["aspirin", "--file", temp_file, "--max-results", "3", "--debug"]
        result = run_cli_command(args, expect_success=False)  # Don't expect success due to missing deps
        
        if result is None:
            print("⚠️  Command execution failed (likely due to missing dependencies)")
            return False
            
        # Check if file was created and has content
        if os.path.exists(temp_file) and os.path.getsize(temp_file) > 0:
            print("✅ Query executed and file created")
            
            # Check CSV content
            with open(temp_file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader, None)
                rows = list(reader)
                
                if headers and "PubmedID" in headers:
                    print(f"✅ CSV format correct, {len(rows)} data rows")
                    return True
                else:
                    print("❌ CSV format incorrect")
                    return False
        else:
            print("⚠️  No output file created (might be expected if no results found)")
            return False
            
    finally:
        # Clean up temp file
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def test_error_handling():
    """Test error handling with invalid parameters."""
    print("\n🧪 Testing error handling...")
    
    # Test invalid max-results
    result = run_cli_command(["test", "--max-results", "-1"], expect_success=False)
    if result and "must be a positive integer" in result.stderr:
        print("✅ Parameter validation works")
        return True
    else:
        print("❌ Parameter validation failed")
        return False

def main():
    """Run all end-to-end tests."""
    print("🚀 Running End-to-End Tests")
    print("=" * 50)
    
    tests = [
        ("Help Functionality", test_help),
        ("Error Handling", test_error_handling),
        ("Simple Query", test_simple_query),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Test {test_name} crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:<20}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your CLI is working correctly.")
    else:
        print("⚠️  Some tests failed. This might be due to missing dependencies.")

if __name__ == "__main__":
    main()