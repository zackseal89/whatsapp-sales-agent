"""
Test script to verify OpenRouter AI is responding.
"""
import asyncio
import sys
sys.path.append('.')

from agents.router import process_message

async def main():
    print("\n" + "="*80)
    print("Testing OpenRouter AI Agent Response")
    print("="*80 + "\n")
    
    # Test message
    test_message = "Hello! I'm interested in buying a laptop. What do you have?"
    print(f"📤 Sending test message: '{test_message}'\n")
    
    try:
        # Call the agent
        response = await process_message(test_message)
        
        print("✅ AGENT RESPONSE RECEIVED:")
        print("-" * 80)
        print(response)
        print("-" * 80)
        
        # Check response quality
        if len(response) > 10:
            print("\n✅ Response looks good! Agent is working.")
        else:
            print("\n⚠️  Response is very short, might be an issue.")
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
