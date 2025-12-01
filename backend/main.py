"""
FastAPI application for WhatsApp AI Sales Agent webhook handling.
"""
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="WhatsApp AI Sales Agent",
    description="AI-powered sales agent for WhatsApp Business",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "WhatsApp AI Sales Agent",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "services": {
            "whatsapp_api": "connected",
            "supabase": "connected",
            "gemini": "connected"
        }
    }


@app.get("/webhooks/whatsapp")
@app.post("/webhooks/whatsapp")
async def whatsapp_webhook_handler(request: Request):
    """
    Handle Twilio WhatsApp webhooks.
    GET: Not used by Twilio (Meta verification only)
    POST: Receive incoming messages
    """
    if request.method == "GET":
        return {"status": "ok", "message": "Twilio uses POST for webhooks"}
    
    # Twilio sends form-encoded data
    form_data = await request.form()
    
    from_number = form_data.get("From", "")  # whatsapp:+254712345678
    message_text = form_data.get("Body", "")
    message_sid = form_data.get("MessageSid", "")
    
    logger.info(f"Received message from {from_number}: {message_text[:50]}...")
    
    # Process the message
    await process_message(from_number, message_text, message_sid)
    
    return Response(content="OK", media_type="text/plain")


async def process_message(from_number: str, message_text: str, message_sid: str):
    """
    Process an incoming WhatsApp message from Twilio.
    
    Args:
        from_number: Sender's number (format: whatsapp:+254712345678)
        message_text: Message content
        message_sid: Twilio message SID
    """
    # Remove "whatsapp:" prefix for database storage
    clean_number = from_number.replace('whatsapp:', '')
    
    logger.info(f"Processing message {message_sid} from {clean_number}")
    
    try:
        # Import Supabase client
        from services.supabase import supabase_client
        
        # 1. Get or create customer
        logger.info(f"Getting/creating customer for {clean_number}")
        customer = await supabase_client.get_or_create_customer(clean_number)
        customer_id = customer['id']
        logger.info(f"Customer ID: {customer_id}")
        
        # 2. Get or create active conversation
        logger.info(f"Getting/creating conversation for customer {customer_id}")
        conversation = await supabase_client.get_or_create_conversation(
            customer_id=customer_id,
            whatsapp_number=clean_number
        )
        conversation_id = conversation['id']
        logger.info(f"Conversation ID: {conversation_id}")
        
        # 3. Store inbound message
        logger.info(f"Storing inbound message")
        await supabase_client.store_message(
            conversation_id=conversation_id,
            direction='inbound',
            message_text=message_text,
            whatsapp_message_id=message_sid,
            sender_type='customer'
        )
        logger.info("Inbound message stored successfully")
        
        # 4. Generate AI response
        logger.info("Generating AI response")
        from agents import process_message as run_agent
        response_text = await run_agent(message_text)
        logger.info(f"AI response generated: {response_text[:100]}...")
        
        # 5. Store outbound message BEFORE sending (for reliability)
        logger.info("Storing outbound message")
        await supabase_client.store_message(
            conversation_id=conversation_id,
            direction='outbound',
            message_text=response_text,
            sender_type='agent'
        )
        logger.info("Outbound message stored successfully")
        
        # 6. Send response via Twilio
        logger.info(f"Sending response to {clean_number}")
        from services.whatsapp import whatsapp_client
        await whatsapp_client.send_text_message(
            to=clean_number,
            message=response_text
        )
        
        logger.info(f"✅ Complete! Customer {customer_id}, Conversation {conversation_id}, Response sent to {clean_number}")
        
    except Exception as e:
        logger.error(f"❌ Error processing message: {str(e)}", exc_info=True)
        # Send user-friendly error message
        try:
            from services.whatsapp import whatsapp_client
            await whatsapp_client.send_text_message(
                to=clean_number,
                message="Sorry, I'm having trouble right now. Please try again in a moment."
            )
        except Exception as send_error:
            logger.error(f"Failed to send error message to user: {send_error}")
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.environment == "development"
    )
