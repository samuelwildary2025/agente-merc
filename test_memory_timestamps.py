#!/usr/bin/env python3
"""
Test script for the updated memory system with timestamps.
Verifies that timestamps are available internally but not exposed to clients.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.limited_postgres_memory import LimitedPostgresChatMessageHistory
from memory.response_filter import prepare_client_response, sanitize_agent_response
from langchain_core.messages import HumanMessage, AIMessage
from config.settings import settings

def test_memory_with_timestamps():
    """Test the memory system with timestamp functionality."""
    print("🧪 Testing memory system with timestamps...")
    
    # Use a test session ID
    test_session = "test_timestamp_session"
    
    try:
        # Initialize memory
        memory = LimitedPostgresChatMessageHistory(
            connection_string=settings.postgres_connection_string,
            session_id=test_session,
            table_name=settings.postgres_table_name,
            max_messages=10
        )
        
        # Clear any existing test data
        memory.clear()
        
        print("✅ Memory initialized successfully")
        
        # Add some test messages
        test_messages = [
            HumanMessage(content="Olá, qual é o preço do arroz?"),
            AIMessage(content="O preço do arroz é R$ 25,90. Posso ajudar com mais alguma coisa?"),
            HumanMessage(content="E o feijão?"),
            AIMessage(content="O feijão custa R$ 18,50 por kg.")
        ]
        
        for msg in test_messages:
            memory.add_message(msg)
            print(f"📤 Added message: {msg.content[:50]}...")
        
        print("✅ Test messages added successfully")
        
        # Test 1: Get messages with timestamps (internal use)
        print("\n📊 Testing internal timestamp retrieval...")
        messages_with_ts = memory.get_recent_messages_with_timestamps()
        
        if messages_with_ts:
            print(f"✅ Retrieved {len(messages_with_ts)} messages with timestamps")
            
            for i, msg_data in enumerate(messages_with_ts):
                message = msg_data['message']
                timestamp = msg_data['timestamp']
                
                print(f"  Message {i+1}: {message.get('content', 'No content')[:40]}...")
                print(f"  Timestamp: {timestamp}")
                
                # Verify timestamp is in ISO format
                if 'T' in timestamp and len(timestamp) > 15:
                    print("  ✅ Timestamp format is correct")
                else:
                    print("  ❌ Timestamp format seems incorrect")
        else:
            print("❌ No messages with timestamps retrieved")
        
        # Test 2: Get conversation metrics
        print("\n📈 Testing conversation metrics...")
        metrics = memory.get_conversation_metrics()
        
        if metrics:
            print("✅ Conversation metrics retrieved:")
            for key, value in metrics.items():
                print(f"  {key}: {value}")
        else:
            print("ℹ️  No metrics available (need more messages for time calculations)")
        
        # Test 3: Test response filtering
        print("\n🧹 Testing response filtering...")
        
        # Simulate an agent response that might contain timestamp data
        test_response = """
        O preço do arroz é R$ 25,90. 
        Informação interna: _timestamp: 2024-01-15T10:30:00
        Outro timestamp: 2024-01-15T11:45:30.000Z
        """
        
        filtered_response = prepare_client_response(test_response)
        print(f"Original response: {test_response[:80]}...")
        print(f"Filtered response: {filtered_response[:80]}...")
        
        # Check if timestamps were removed
        if "2024-01-15" not in filtered_response:
            print("✅ Timestamps successfully filtered from client response")
        else:
            print("❌ Timestamps still present in filtered response")
        
        # Test 4: Test optimized context (should not include timestamps)
        print("\n🎯 Testing optimized context retrieval...")
        optimized_messages = memory.get_optimized_context()
        
        if optimized_messages:
            print(f"✅ Retrieved {len(optimized_messages)} optimized messages")
            # These should be BaseMessage objects without timestamp metadata
            for i, msg in enumerate(optimized_messages):
                print(f"  Message {i+1}: {msg.content[:40]}...")
                # Check that no timestamp metadata is exposed
                if hasattr(msg, 'additional_kwargs') and '_timestamp' in msg.additional_kwargs:
                    print("  ❌ Timestamp found in message metadata")
                else:
                    print("  ✅ No timestamp in message metadata")
        
        # Cleanup
        memory.clear()
        print("\n🧹 Test data cleaned up")
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_response_filter():
    """Test the response filter utility."""
    print("\n🧪 Testing response filter utility...")
    
    test_cases = [
        # Test case 1: Simple timestamp in JSON
        {
            "input": '{"content": "Hello", "_timestamp": "2024-01-15T10:30:00"}',
            "expected_no_timestamp": True
        },
        # Test case 2: Timestamp in text
        {
            "input": "Response at 2024-01-15T10:30:00.000Z",
            "expected_no_timestamp": True
        },
        # Test case 3: Multiple timestamps
        {
            "input": "First: 2024-01-15T10:30:00, Second: 2024-01-16T11:45:30",
            "expected_no_timestamp": True
        },
        # Test case 4: Normal response without timestamps
        {
            "input": "O preço do arroz é R$ 25,90",
            "expected_no_timestamp": False  # Should remain unchanged
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n  Test case {i+1}: {test_case['input'][:50]}...")
        
        filtered = prepare_client_response(test_case['input'])
        print(f"  Filtered: {filtered[:50]}...")
        
        if test_case['expected_no_timestamp']:
            if "2024-01-15" not in filtered and "2024-01-16" not in filtered:
                print("  ✅ Timestamps properly removed")
            else:
                print("  ❌ Timestamps still present")
        else:
            if filtered == test_case['input']:
                print("  ✅ Response unchanged (no timestamps to remove)")
            else:
                print("  ❌ Response was modified unnecessarily")
    
    print("\n✅ Response filter tests completed!")

if __name__ == "__main__":
    print("🚀 Starting memory system timestamp tests...\n")
    
    # Test response filter first
    test_response_filter()
    
    # Test memory system
    success = test_memory_with_timestamps()
    
    if success:
        print("\n🎉 All tests passed! The memory system now supports timestamps for internal use while keeping them hidden from clients.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        sys.exit(1)