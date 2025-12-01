# Phase 2: Core AI Agent Implementation

## Overview

**Goal**: Build the foundational AI agent system with Google ADK, implement the Router and Product Search agents, connect Twilio WhatsApp API, and enable basic conversational product search.

**Timeline**: Week 3-4 (2 weeks)

**Prerequisites**:
- ✅ Database schema deployed on Supabase
- ✅ Backend FastAPI structure in place
- ✅ Twilio WhatsApp account set up
- ⏳ Environment variables configured

---

## Week 3: Basic Agent Setup & Twilio Integration

### Day 1-2: Twilio WhatsApp Integration

**Tasks**:
- [ ] Sign up for Twilio account
- [ ] Get WhatsApp sandbox credentials
- [ ] Update `backend/requirements.txt` to include `twilio`
- [ ] Update `backend/config.py` with Twilio settings
- [ ] Rewrite `backend/services/whatsapp.py` for Twilio
- [ ] Test sending/receiving messages via sandbox

**Deliverables**:
- Working Twilio WhatsApp connection
- Can send and receive test messages
- Webhook receives messages from Twilio

**Testing**:
```bash
# Send test message from your phone to Twilio sandbox
# Should see webhook receive message in backend logs
# Backend should echo message back
```

---

### Day 3-4: Google ADK Setup & Router Agent

**Tasks**:
- [ ] Install Google ADK: `pip install google-adk`
- [ ] Create `backend/agents/` directory structure
- [ ] Implement basic Router Agent
- [ ] Configure Gemini Pro model
- [ ] Test agent with simple prompts

**File**: `backend/agents/router.py`

```python
"""
Router Agent - Main conversation orchestrator.
"""
from google.adk.llm import LlmAgent
from google.adk.runners import run_agent
from google.genai import types

# Configure Router Agent
router_agent = LlmAgent(
    model="gemini/gemini-2.0-flash-exp",
    system_instruction="""
    You are a friendly WhatsApp sales assistant for an e-commerce business.
    
    Your job is to:
    1. Greet customers warmly
    2. Understand what they're looking for
    3. Help them find products
    4. Guide them through ordering
    
    Be conversational, helpful, and enthusiastic!
    """,
    generation_config=types.GenerationConfig(
        temperature=0.7,
        top_p=0.95,
        max_output_tokens=500,
    )
)


async def process_customer_message(message: str, session_id: str = None):
    """
    Process incoming customer message through router agent.
    
    Args:
        message: Customer's message text
        session_id: Session ID for context retention
        
    Returns:
        Agent's response
    """
    response = await run_agent(
        agent=router_agent,
        user_message=message,
        session_id=session_id
    )
    
    return response.content
```

**File**: `backend/agents/__init__.py`

```python
"""AI Agents module."""
from .router import router_agent, process_customer_message

__all__ = ["router_agent", "process_customer_message"]
```

**Testing**:
- Test router agent with various greetings
- Verify conversation flow
- Check context retention across messages

---

### Day 5: Integrate Router Agent with WhatsApp Webhook

**Tasks**:
- [ ] Update `main.py` to call router agent
- [ ] Implement session management for context
- [ ] Store messages in database
- [ ] Handle errors gracefully

**File Update**: `backend/main.py`

```python
from agents import process_customer_message
from services.supabase import supabase_client
from services.whatsapp import whatsapp_client

@app.post("/webhooks/whatsapp")
async def whatsapp_webhook(request: Request):
    """Handle Twilio WhatsApp messages."""
    form_data = await request.form()
    
    from_number = form_data.get("From").replace('whatsapp:', '')
    message_text = form_data.get("Body")
    message_sid = form_data.get("MessageSid")
    
    try:
        # Get/create customer
        customer = await supabase_client.get_customer_by_whatsapp(from_number)
        if not customer:
            customer = await supabase_client.create_customer(from_number)
        
        # Get/create conversation
        conversation = await supabase_client.get_active_conversation(customer['id'])
        if not conversation:
            conversation = await supabase_client.create_conversation(
                customer['id'],
                from_number
            )
        
        # Store inbound message
        await supabase_client.store_message(
            conversation_id=conversation['id'],
            direction='inbound',
            message_text=message_text,
            whatsapp_message_id=message_sid,
            sender_type='customer'
        )
        
        # Process with AI agent
        response = await process_customer_message(
            message=message_text,
            session_id=conversation['id']
        )
        
        # Send response via Twilio
        await whatsapp_client.send_text_message(
            to=f"whatsapp:{from_number}",
            message=response
        )
        
        # Store outbound message
        await supabase_client.store_message(
            conversation_id=conversation['id'],
            direction='outbound',
            message_text=response,
            sender_type='agent',
            agent_name='router'
        )
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        # Send error message to customer
        await whatsapp_client.send_text_message(
            to=f"whatsapp:{from_number}",
            message="Sorry, I'm having trouble right now. Please try again in a moment."
        )
        return {"status": "error", "detail": str(e)}
```

**Testing**:
- Send message to WhatsApp sandbox
- Verify agent responds
- Check messages are stored in database
- Test conversation context retention

---

## Week 4: Product Search Agent & MCP Integration

### Day 1-2: Supabase MCP Connection

**Tasks**:
- [ ] Configure Supabase MCP in ADK
- [ ] Test MCP connection to database
- [ ] Create product search tools
- [ ] Test database queries via MCP

**File**: `backend/services/mcp_tools.py`

```python
"""
Supabase MCP tools for product operations.
"""
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams
from config import settings

# Initialize Supabase MCP connection
supabase_mcp = McpToolset(
    connection_params=SseConnectionParams(
        url=f"https://mcp.supabase.com/mcp?project_ref={settings.supabase_project_ref}"
    )
)
```

**Testing**:
```python
# Test MCP connection
result = await supabase_mcp.execute_query(
    "SELECT * FROM products WHERE is_active = true LIMIT 5"
)
print(result)
```

---

### Day 3-4: Product Search Agent Implementation

**Tasks**:
- [ ] Create Product Search Agent
- [ ] Add product search tools (MCP)
- [ ] Implement natural language product search
- [ ] Add product recommendation logic

**File**: `backend/agents/product_search.py`

```python
"""
Product Search Agent - Helps customers find products.
"""
from google.adk.llm import LlmAgent
from google.genai import types
from services.mcp_tools import supabase_mcp

product_search_agent = LlmAgent(
    model="gemini/gemini-2.0-flash-exp",
    system_instruction="""
    You are a product specialist helping customers find items.
    
    When a customer describes what they want:
    1. Use search_products tool to find matching items
    2. Present top 3-5 results with key details (name, price, description)
    3. Ask if they want more details or to see other options
    4. Be enthusiastic about the products!
    
    Format product lists clearly:
    📦 [Product Name] - $[Price]
       [Brief description]
    """,
    tools=[supabase_mcp],  # Has access to database
    generation_config=types.GenerationConfig(
        temperature=0.6,
        max_output_tokens=600,
    )
)
```

**Testing**:
- "Show me laptops"
- "I need running shoes under $100"
- "What smartphones do you have?"

---

### Day 5: Router ↔ Product Agent Integration

**Tasks**:
- [ ] Update Router to transfer to Product Agent
- [ ] Implement intent detection for product queries
- [ ] Test agent handoff
- [ ] Verify conversation flow

**File Update**: `backend/agents/router.py`

```python
from google.adk.tools import AgentTool
from .product_search import product_search_agent

router_agent = LlmAgent(
    model="gemini/gemini-2.0-flash-exp",
    system_instruction="""
    You are the main sales assistant router.
    
    When customers ask about products, finding items, or browsing:
    → Transfer to Product Search Agent
    
    For greetings and general questions:
    → Handle yourself with friendly responses
    
    Always be warm and helpful!
    """,
    tools=[
        AgentTool(product_search_agent, name="product_search")
    ]
)
```

---

## Success Criteria

### End of Week 3:
- ✅ Twilio WhatsApp integration working
- ✅ Can send/receive messages
- ✅ Router agent responds to greetings
- ✅ Messages stored in database
- ✅ Conversation context works

### End of Week 4:
- ✅ MCP connection to Supabase working
- ✅ Product Search Agent finds products
- ✅ Router correctly hands off to Product Agent
- ✅ Customers can search and browse products via WhatsApp
- ✅ Full conversation history captured

---

## Testing Checklist

**Functional Tests**:
- [ ] Send "Hi" → Get welcome response
- [ ] Ask "Show me phones" → Get product list
- [ ] Ask "Tell me about [product]" → Get details
- [ ] Multi-turn conversation maintains context
- [ ] Database stores all messages correctly

**Error Handling**:
- [ ] Invalid product search returns helpful message
- [ ] Network errors handled gracefully
- [ ] Twilio API errors caught and logged

---

## Deliverables

1. **Working AI Agents**:
   - Router Agent (conversation orchestrator)
   - Product Search Agent (uses MCP for database)

2. **Twilio Integration**:
   - Send/receive WhatsApp messages
   - Webhook handling
   - Error handling

3. **Database Integration**:
   - Messages stored
   - Conversations tracked
   - Customer profiles created

4. **Documentation**:
   - Setup instructions
   - Testing guide
   - Known limitations

---

## Next Phase Preview

**Phase 3 (Weeks 5-6)**: Specialized Agents
- Greeter Agent (welcome new customers)
- Cart & Order Agent (checkout process)
- Support Agent (order tracking, returns)
- Escalation Agent (human handoff)

Ready to start Phase 2 implementation!
