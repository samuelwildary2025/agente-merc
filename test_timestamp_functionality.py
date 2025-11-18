#!/usr/bin/env python3
"""
Test script for the memory system timestamp functionality.
Tests the filtering and internal timestamp handling without requiring database connection.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.response_filter import prepare_client_response, sanitize_agent_response
from datetime import datetime

def test_response_filter():
    """Test the response filter utility."""
    print("🧪 Testing response filter utility...")
    
    test_cases = [
        # Test case 1: Simple timestamp in JSON
        {
            "input": '{"content": "Hello", "_timestamp": "2024-01-15T10:30:00"}',
            "expected_no_timestamp": True,
            "description": "JSON with timestamp field"
        },
        # Test case 2: Timestamp in text
        {
            "input": "Response at 2024-01-15T10:30:00.000Z",
            "expected_no_timestamp": True,
            "description": "Text with ISO timestamp"
        },
        # Test case 3: Multiple timestamps
        {
            "input": "First: 2024-01-15T10:30:00, Second: 2024-01-16T11:45:30",
            "expected_no_timestamp": True,
            "description": "Multiple timestamps in text"
        },
        # Test case 4: Normal response without timestamps
        {
            "input": "O preço do arroz é R$ 25,90",
            "expected_no_timestamp": False,  # Should remain unchanged
            "description": "Normal text without timestamps"
        },
        # Test case 5: Agent response with internal metadata
        {
            "input": "Baseado no histórico às 2024-01-15T14:30:00, o cliente perguntou sobre arroz",
            "expected_no_timestamp": True,
            "description": "Agent response mentioning timestamp"
        },
        # Test case 6: Complex JSON with nested timestamps
        {
            "input": '{"response": "OK", "metadata": {"_timestamp": "2024-01-15T10:30:00", "user": "client"}}',
            "expected_no_timestamp": True,
            "description": "Complex JSON with nested timestamp"
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases):
        print(f"\n  Test {i+1}: {test_case['description']}")
        print(f"    Input: {test_case['input'][:60]}...")
        
        filtered = prepare_client_response(test_case['input'])
        print(f"    Output: {filtered[:60]}...")
        
        if test_case['expected_no_timestamp']:
            # Check that no ISO timestamps remain
            iso_pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
            import re
            if not re.search(iso_pattern, filtered):
                print("    ✅ Timestamps properly removed")
            else:
                print("    ❌ Timestamps still present")
                all_passed = False
        else:
            if filtered == test_case['input']:
                print("    ✅ Response unchanged (no timestamps to remove)")
            else:
                print("    ❌ Response was modified unnecessarily")
                all_passed = False
    
    return all_passed

def test_timestamp_utilities():
    """Test timestamp-related utility functions."""
    print("\n🧪 Testing timestamp utilities...")
    
    # Test ISO format validation
    test_timestamp = datetime.now().isoformat()
    print(f"  Current timestamp: {test_timestamp}")
    
    # Test sanitization of different data types
    test_data = [
        {"type": "string", "data": f"Response generated at {test_timestamp}"},
        {"type": "dict", "data": {"content": "Hello", "_timestamp": test_timestamp}},
        {"type": "list", "data": ["item1", f"timestamp: {test_timestamp}", "item3"]},
        {"type": "mixed", "data": {"response": "OK", "items": [f"time: {test_timestamp}", "data"]}},
    ]
    
    all_passed = True
    
    for test in test_data:
        print(f"\n  Testing {test['type']} sanitization:")
        print(f"    Before: {str(test['data'])[:60]}...")
        
        sanitized = sanitize_agent_response(test['data'])
        print(f"    After: {str(sanitized)[:60]}...")
        
        # Check if timestamp was removed
        if test_timestamp not in str(sanitized):
            print("    ✅ Timestamp properly sanitized")
        else:
            print("    ❌ Timestamp still present")
            all_passed = False
    
    return all_passed

def test_internal_vs_external_data():
    """Test the distinction between internal and external data."""
    print("\n🧪 Testing internal vs external data handling...")
    
    # Simulate internal data that agent might use
    internal_data = {
        "message": "O cliente perguntou sobre arroz",
        "_timestamp": "2024-01-15T10:30:00",
        "_session_duration": 15.5,
        "_confidence": 0.85
    }
    
    print(f"  Internal data: {str(internal_data)[:60]}...")
    
    # Sanitize for external use
    external_data = sanitize_agent_response(internal_data)
    print(f"  External data: {str(external_data)[:60]}...")
    
    # Verify internal fields were removed
    internal_fields = ["_timestamp", "_session_duration", "_confidence"]
    removed_all = all(field not in str(external_data) for field in internal_fields)
    
    if removed_all:
        print("  ✅ All internal fields properly removed")
        return True
    else:
        print("  ❌ Some internal fields still present")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting memory system timestamp tests...\n")
    
    # Test response filter
    filter_passed = test_response_filter()
    
    # Test timestamp utilities
    utils_passed = test_timestamp_utilities()
    
    # Test internal vs external data handling
    data_passed = test_internal_vs_external_data()
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    
    tests = [
        ("Response Filter", filter_passed),
        ("Timestamp Utilities", utils_passed),
        ("Internal vs External Data", data_passed)
    ]
    
    all_passed = True
    for test_name, passed in tests:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("="*50)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ The memory system now supports timestamps for internal use")
        print("✅ Timestamps are properly hidden from client responses")
        print("✅ Internal metadata is sanitized before external exposure")
    else:
        print("❌ SOME TESTS FAILED")
        print("Please review the implementation")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)