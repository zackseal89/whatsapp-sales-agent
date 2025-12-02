"""
Quick test script to see what the agent actually responds with.
"""
import asyncio
import sys
sys.path.append('.')

from agents import process_message

async def main():
    test_message = "I want to order 1 laptop"
    response = await process_message(test_message)
    print("\n" + "="*80)
    print("AGENT RESPONSE:")
    print("="*80)
    print(response)
    print("="*80)
    
    # Check for ORDER_DETAILS tag
    if '<ORDER_DETAILS>' in response:
        print("\n✅ ORDER_DETAILS tag FOUND in response")
    else:
        print("\n❌ ORDER_DETAILS tag NOT FOUND in response")
    print("="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
