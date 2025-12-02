"""
Test the memory system with a simulated conversation
"""
import asyncio
import sys
sys.path.append('.')

from services.supabase import supabase_client
from agents import process_message as run_agent

async def main():
    print("\n" + "="*80)
    print("Testing Memory System")
    print("="*80 + "\n")
    
    # Use the specific conversation where "My name is zack" was sent
    conv_id = "861731c8-1719-4a80-9cd1-2441f9489d67"
    print(f"Using conversation: {conv_id}\n")
    
    # Fetch history
    history = await supabase_client.get_recent_messages(conv_id, limit=10)
    
    print(f"📋 Retrieved {len(history)} messages from history:")
    print("-" * 80)
    for msg in history:
        sender = "AGENT" if msg.get("sender_type") == "agent" else "USER"
        print(f"  {sender}: {msg.get('message_text', '')[:60]}...")
    print()
    
    # Test with new message
    test_message = "What is my name?"
    print(f"🧪 Testing with message: '{test_message}'")
    print()
    
    # Call agent with history
    response = await run_agent(test_message, message_history=history)
    
    print("🤖 Agent Response:")
    print("-" * 80)
    print(response)
    print("-" * 80)
    
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
