"""
Supabase client for database operations.
Uses Supabase Python SDK with service role key for admin access.
"""
from supabase import create_client, Client
from config import settings
from services.cache import cache
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class SupabaseClient:
    """Supabase database client with admin access."""
    
    def __init__(self):
        """Initialize Supabase client with service role key."""
        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_key
        )
        logger.info("Supabase client initialized")
    
    async def get_or_create_customer(self, whatsapp_number: str) -> Dict[str, Any]:
        """
        Get existing customer or create new one.
        
        Args:
            whatsapp_number: Customer's WhatsApp number (without 'whatsapp:' prefix)
            
        Returns:
            Customer record dict with id, whatsapp_number, etc.
        """
        try:
            # Check cache first
            cached_customer = await cache.get_cached_customer(whatsapp_number)
            if cached_customer:
                logger.info(f"Cache hit for customer: {whatsapp_number}")
                return cached_customer

            # Try to find existing customer
            result = self.client.table('customers').select('*').eq(
                'whatsapp_number', whatsapp_number
            ).limit(1).execute()
            
            if result.data and len(result.data) > 0:
                customer = result.data[0]
                logger.info(f"Found existing customer: {customer['id']}")
                # Cache the result
                await cache.set_cached_customer(
                    whatsapp_number, 
                    customer, 
                    ttl=settings.redis_ttl_customer_data
                )
                return customer
            
            # Create new customer
            new_customer = self.client.table('customers').insert({
                'whatsapp_number': whatsapp_number
            }).execute()
            
            customer = new_customer.data[0]
            logger.info(f"Created new customer: {customer['id']}")
            
            # Cache the new customer
            await cache.set_cached_customer(
                whatsapp_number, 
                customer, 
                ttl=settings.redis_ttl_customer_data
            )
            return customer
            
        except Exception as e:
            logger.error(f"Error in get_or_create_customer: {str(e)}")
            raise
    
    async def get_or_create_conversation(
        self, 
        customer_id: str, 
        whatsapp_number: str
    ) -> Dict[str, Any]:
        """
        Get active conversation or create new one.
        
        Args:
            customer_id: Customer UUID
            whatsapp_number: Customer's WhatsApp number
            
        Returns:
            Conversation record dict
        """
        try:
            # Look for active conversation
            result = self.client.table('conversations').select('*').eq(
                'customer_id', customer_id
            ).eq(
                'status', 'active'
            ).order('started_at', desc=True).limit(1).execute()
            
            if result.data and len(result.data) > 0:
                logger.info(f"Found active conversation: {result.data[0]['id']}")
                return result.data[0]
            
            # Create new conversation
            new_conversation = self.client.table('conversations').insert({
                'customer_id': customer_id,
                'whatsapp_number': whatsapp_number,
                'status': 'active'
            }).execute()
            
            logger.info(f"Created new conversation: {new_conversation.data[0]['id']}")
            return new_conversation.data[0]
            
        except Exception as e:
            logger.error(f"Error in get_or_create_conversation: {str(e)}")
            raise
    
    async def store_message(
        self,
        conversation_id: str,
        direction: str,
        message_text: str,
        whatsapp_message_id: Optional[str] = None,
        sender_type: str = "customer"
    ) -> Dict[str, Any]:
        """
        Store a message in the database.
        
        Args:
            conversation_id: Conversation UUID
            direction: 'inbound' or 'outbound'
            message_text: Message content
            whatsapp_message_id: Twilio message SID (optional)
            sender_type: 'customer' or 'agent'
            
        Returns:
            Created message record
        """
        try:
            message_data = {
                'conversation_id': conversation_id,
                'direction': direction,
                'message_text': message_text,
                'sender_type': sender_type,
                'is_automated': sender_type == 'agent'
            }
            
            if whatsapp_message_id:
                message_data['whatsapp_message_id'] = whatsapp_message_id
            
            result = self.client.table('messages').insert(message_data).execute()
            
            logger.info(f"Stored {direction} message in conversation {conversation_id}")
            return result.data[0]
            
        except Exception as e:
            logger.error(f"Error in store_message: {str(e)}")
            raise
    
    async def search_products(
        self, 
        search_query: str, 
        limit: int = 10
    ) -> list[Dict[str, Any]]:
        """
        Search for products (for future Product Search Agent).
        
        Args:
            search_query: Search term
            limit: Maximum results
            
        Returns:
            List of product records
        """
        try:
            result = self.client.table('products').select('*').eq(
                'is_active', True
            ).or_(
                f'name.ilike.%{search_query}%,description.ilike.%{search_query}%'
            ).limit(limit).execute()
            
            logger.info(f"Found {len(result.data)} products matching '{search_query}'")
            return result.data
            
        except Exception as e:
            logger.error(f"Error in search_products: {str(e)}")
            raise

    async def create_order(
        self,
        customer_id: str,
        items: list[Dict[str, Any]],
        total: float
    ) -> Dict[str, Any]:
        """
        Create a new order.
        
        Args:
            customer_id: Customer UUID
            items: List of order items
            total: Total order amount
            
        Returns:
            Created order record
        """
        try:
            # Generate a simple order number (timestamp based for MVP)
            import time
            order_number = f"ORD-{int(time.time())}"
            
            order_data = {
                'customer_id': customer_id,
                'status': 'pending_payment',
                'total': total,
                'items': items,
                'order_number': order_number
            }
            
            result = self.client.table('orders').insert(order_data).execute()
            
            logger.info(f"Created order {order_number} for customer {customer_id}")
            return result.data[0]
            
        except Exception as e:
            logger.error(f"Error in create_order: {str(e)}")
            raise

    async def get_recent_messages(
        self,
        conversation_id: str,
        limit: int = 10
    ) -> list[Dict[str, Any]]:
        """
        Get recent messages for a conversation.
        
        Args:
            conversation_id: Conversation UUID
            limit: Number of messages to retrieve
            
        Returns:
            List of message records, ordered by created_at asc
        """
        try:
            result = self.client.table('messages').select('*').eq(
                'conversation_id', conversation_id
            ).order('created_at', desc=True).limit(limit).execute()
            
            # Return reversed list (oldest first) for context
            messages = result.data[::-1] if result.data else []
            logger.info(f"Retrieved {len(messages)} recent messages for conversation {conversation_id}")
            return messages
            
        except Exception as e:
            logger.error(f"Error in get_recent_messages: {str(e)}")
            return []


# Global Supabase client instance
supabase_client = SupabaseClient()
