"""
Quick script to check the conversation history in the database
"""
import asyncio
import sys
sys.path.append('.')

from services.supabase import supabase_client

async def main():
    print("\n" + "="*80)
    print("Checking Recent Conversations and Messages")
    print("="*80 + "\n")
    
    try:
        # Get recent conversations
        result = supabase_client.client.table('conversations').select('*').order('started_at', desc=True).limit(1).execute()
        
        if result.data and len(result.data) > 0:
            conv = result.data[0]
            print(f"📝 Latest Conversation: {conv['id']}")
            print(f"   Customer: {conv['customer_id']}")
            print(f"   Status: {conv['status']}")
            print(f"   Started: {conv['started_at']}")
            print()
            
            # Get messages for this conversation
            messages = supabase_client.client.table('messages').select('*').eq(
                'conversation_id', conv['id']
            ).order('created_at', desc=False).execute()
            
            print(f"💬 Messages ({len(messages.data)}):")
            print("-" * 80)
            for i, msg in enumerate(messages.data, 1):
                sender = "🤖 AGENT" if msg['sender_type'] == 'agent' else "👤 USER"
                print(f"{i}. {sender} [{msg['created_at']}]")
                print(f"   {msg['message_text'][:100]}")
                print()
                
        else:
            print("No conversations found")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
