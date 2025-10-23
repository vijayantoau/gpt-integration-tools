#!/usr/bin/env python3
"""
Test runner for GPT Integration Tools
"""

import os
import sys
import subprocess
import json

def run_test(test_file, description):
    """Run a test file and report results"""
    print(f"\n🧪 Running {description}...")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} - FAILED")
            if result.stderr:
                print(f"Error: {result.stderr}")
            if result.stdout:
                print(f"Output: {result.stdout}")
                
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT")
    except Exception as e:
        print(f"💥 {description} - ERROR: {e}")

def main():
    """Main test runner"""
    print("🚀 GPT Integration Tools - Test Suite")
    print("=" * 60)
    
    # Change to tests directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Test files and descriptions
    tests = [
        ("simple_tool_test.py", "Simple Tool Call Flow Test"),
        ("debug_tool_calls.py", "Debug Tool Calls Test (requires OpenAI API key)"),
        ("chatgpt_sdk_example.py", "ChatGPT SDK Integration Test (requires OpenAI API key)"),
    ]
    
    # Check for OpenAI API key
    has_api_key = bool(os.getenv('OPENAI_API_KEY'))
    print(f"🔑 OpenAI API Key: {'✅ Available' if has_api_key else '❌ Not set'}")
    
    if not has_api_key:
        print("\n⚠️  Some tests require OPENAI_API_KEY environment variable")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
    
    # Run tests
    passed = 0
    total = 0
    
    for test_file, description in tests:
        if os.path.exists(test_file):
            total += 1
            run_test(test_file, description)
            
            # Check if test passed (simple heuristic)
            if "PASSED" in str(subprocess.run([sys.executable, test_file], 
                                            capture_output=True, text=True, timeout=5)):
                passed += 1
        else:
            print(f"⚠️  Test file not found: {test_file}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed or require API key")
        return 1

if __name__ == "__main__":
    sys.exit(main())
