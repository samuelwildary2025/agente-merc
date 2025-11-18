#!/usr/bin/env python3
"""
Demonstration script showing how the agent can use timestamps internally.
This shows the practical usage of timestamp data for agent analysis.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.limited_postgres_memory import LimitedPostgresChatMessageHistory
from memory.response_filter import prepare_client_response
from datetime import datetime
from config.settings import settings

def demonstrate_timestamp_usage():
    """Demonstrate how timestamps can be used for internal agent analysis."""
    print("🎯 Demonstrating timestamp usage for agent internal analysis...\n")
    
    # Simulate some conversation data with timestamps
    mock_messages = [
        {
            "message": {"type": "human", "content": "Olá, qual é o preço do arroz?"},
            "timestamp": "2024-01-15T10:00:00"
        },
        {
            "message": {"type": "ai", "content": "O arroz custa R$ 25,90. Posso ajudar com mais algo?"},
            "timestamp": "2024-01-15T10:00:15"
        },
        {
            "message": {"type": "human", "content": "E o feijão?"},
            "timestamp": "2024-01-15T10:02:30"
        },
        {
            "message": {"type": "ai", "content": "O feijão custa R$ 18,50 por kg."},
            "timestamp": "2024-01-15T10:02:45"
        },
        {
            "message": {"type": "human", "content": "Tem desconto se eu comprar os dois?"},
            "timestamp": "2024-01-15T10:05:00"
        }
    ]
    
    print("📊 Example: Analyzing conversation patterns with timestamps")
    print("=" * 60)
    
    # Analyze response times
    response_times = []
    for i in range(1, len(mock_messages)):
        if mock_messages[i]["message"]["type"] == "ai":
            # Calculate time difference from previous human message
            prev_time = datetime.fromisoformat(mock_messages[i-1]["timestamp"])
            curr_time = datetime.fromisoformat(mock_messages[i]["timestamp"])
            response_time = (curr_time - prev_time).total_seconds()
            response_times.append(response_time)
            
            print(f"Agent response {i//2 + 1}: {response_time:.1f} seconds")
    
    if response_times:
        avg_response_time = sum(response_times) / len(response_times)
        print(f"\nAverage agent response time: {avg_response_time:.1f} seconds")
        
        # Analyze conversation flow
        print(f"Total conversation time: {(datetime.fromisoformat(mock_messages[-1]['timestamp']) - datetime.fromisoformat(mock_messages[0]['timestamp'])).total_seconds() / 60:.1f} minutes")
        print(f"Number of exchanges: {len([m for m in mock_messages if m['message']['type'] == 'ai'])}")
    
    print("\n" + "=" * 60)
    print("🤖 Example: Agent using timestamp data for context")
    print("=" * 60)
    
    # Simulate agent analysis using timestamps
    recent_time = datetime.fromisoformat(mock_messages[-1]["timestamp"])
    first_time = datetime.fromisoformat(mock_messages[0]["timestamp"])
    
    conversation_duration = (recent_time - first_time).total_seconds() / 60
    
    if conversation_duration > 5:
        agent_analysis = f"Esta conversa já dura {conversation_duration:.0f} minutos. O cliente parece estar comparando produtos."
    else:
        agent_analysis = "Conversa recente, cliente está começando a explorar os produtos."
    
    print(f"Agent internal analysis: {agent_analysis}")
    
    # Show how this would be filtered for client
    client_response = prepare_client_response(agent_analysis)
    print(f"Client response (filtered): {client_response}")
    
    print("\n" + "=" * 60)
    print("🔍 Example: Detecting conversation patterns")
    print("=" * 60)
    
    # Analyze gaps in conversation
    time_gaps = []
    for i in range(1, len(mock_messages)):
        prev_time = datetime.fromisoformat(mock_messages[i-1]["timestamp"])
        curr_time = datetime.fromisoformat(mock_messages[i]["timestamp"])
        gap = (curr_time - prev_time).total_seconds()
        time_gaps.append(gap)
        
        if gap > 120:  # More than 2 minutes
            print(f"⏰ Long pause detected: {gap:.0f} seconds between messages {i} and {i+1}")
            print(f"   Previous: {mock_messages[i-1]['message']['content'][:30]}...")
            print(f"   Current: {mock_messages[i]['message']['content'][:30]}...")
    
    print("\n" + "=" * 60)
    print("✅ Key Benefits of Timestamp Integration:")
    print("• Agent can analyze conversation flow and response patterns")
    print("• Long pauses can indicate customer hesitation or comparison shopping")
    print("• Response time analysis helps optimize agent performance")
    print("• Conversation duration helps understand customer engagement")
    print("• All timestamp data stays internal - never exposed to clients")
    print("=" * 60)

if __name__ == "__main__":
    demonstrate_timestamp_usage()