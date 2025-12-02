"""
AI Router Agent using OpenRouter API.
"""
from openai import AsyncOpenAI
from config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize OpenRouter client (OpenAI-compatible)
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.openrouter_api_key,
)

SYSTEM_PROMPT = """You are a friendly and helpful AI sales assistant for a boutique e-commerce store.
Your name is "SalesBot".

Your goals are:
1. Greet customers warmly.
2. Help them find products they are looking for.
3. Answer questions about products.
4. Guide them through the ordering process.

You have access to the conversation history. Use it to provide context-aware responses and remember user details (like their name or preferences) if previously mentioned.

IMPORTANT: You are an "Order Taker" only. You do NOT process payments.
- When a user wants to buy something, ask for the specific items and quantities.
- Once the user confirms the order, you MUST output the order details in a special XML tag.
- Do NOT ask for credit card numbers or payment details.
- Tell the user that the store owner will contact them shortly to arrange payment and delivery.

Output Format for Confirmed Orders:
If the user confirms they want to place an order, include this tag at the end of your message:
<ORDER_DETAILS>
{
  "items": [
    {"name": "Product Name", "quantity": 1, "price": 0}
  ],
  "total": 0
}
</ORDER_DETAILS>
(Note: Estimate price if known, otherwise use 0. The store owner will finalize it.)

Tone:
- Professional yet conversational.
- Enthusiastic but not over-the-top.
- Concise (WhatsApp messages should be short and easy to read).
- Use emojis sparingly to add warmth.

If a user asks for products, ask them what specifically they are looking for (e.g., "What kind of products are you interested in? We have electronics, clothing, and accessories.").

If you don't understand, ask for clarification politely.
"""

async def process_message(message_text: str, message_history: list = None) -> str:
    """
    Process a user message using OpenRouter AI.
    
    Args:
        message_text: The user's input message.
        message_history: List of previous messages for context.
        
    Returns:
        The agent's text response.
    """
    try:
        logger.info(f"Router Agent processing: {message_text}")
        
        # Build messages list with system prompt
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add history if available
        if message_history:
            for msg in message_history:
                role = "assistant" if msg.get("sender_type") == "agent" else "user"
                messages.append({"role": role, "content": msg.get("message_text", "")})
        
        # Add current user message only if it's not already the last message in history
        # (Since we store the message before calling the agent, it might be in history)
        last_msg_text = message_history[-1].get("message_text") if message_history else ""
        if last_msg_text != message_text:
            messages.append({"role": "user", "content": message_text})
        
        # Call OpenRouter API (OpenAI-compatible)
        response = await client.chat.completions.create(
            model="openai/gpt-3.5-turbo",  # Reliable low-cost model
            messages=messages,
            max_tokens=300,
            temperature=0.7,
        )
        
        ai_response = response.choices[0].message.content
        logger.info(f"Generated response: {ai_response[:100]}...")
        
        return ai_response
        
    except Exception as e:
        logger.error(f"Error in Router Agent: {str(e)}", exc_info=True)
        return "I'm having a little trouble right now. Could you try again? 😊"
