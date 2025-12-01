"""
Twilio WhatsApp API client for sending messages.
"""
from twilio.rest import Client
from config import settings
import logging

logger = logging.getLogger(__name__)


class WhatsAppClient:
    """Twilio WhatsApp API client."""
    
    def __init__(self):
        """Initialize Twilio client."""
        self.client = Client(
            settings.twilio_account_sid,
            settings.twilio_auth_token
        )
        self.from_number = settings.twilio_whatsapp_number
    
    async def send_text_message(self, to: str, message: str):
        """
        Send a text message via Twilio WhatsApp.
        
        Args:
            to: Recipient's WhatsApp number (format: +254712345678 or whatsapp:+254712345678)
            message: Message text to send
            
        Returns:
            Message SID and status
        """
        try:
            # Ensure "whatsapp:" prefix
            if not to.startswith('whatsapp:'):
                to = f'whatsapp:{to}'
            
            msg = self.client.messages.create(
                from_=self.from_number,
                body=message,
                to=to
            )
            
            logger.info(f"Message sent to {to}: SID {msg.sid}")
            return {
                "status": "sent",
                "message_sid": msg.sid,
                "to": to
            }
            
        except Exception as e:
            logger.error(f"Failed to send message to {to}: {str(e)}")
            raise
    
    async def send_media_message(self, to: str, message: str, media_url: str):
        """
        Send a message with media (image, video, etc.).
        
        Args:
            to: Recipient's WhatsApp number
            message: Message caption
            media_url: URL of the media to send
            
        Returns:
            Message SID and status
        """
        try:
            if not to.startswith('whatsapp:'):
                to = f'whatsapp:{to}'
            
            msg = self.client.messages.create(
                from_=self.from_number,
                body=message,
                media_url=[media_url],
                to=to
            )
            
            logger.info(f"Media message sent to {to}: SID {msg.sid}")
            return {
                "status": "sent",
                "message_sid": msg.sid,
                "to": to
            }
            
        except Exception as e:
            logger.error(f"Failed to send media message to {to}: {str(e)}")
            raise


# Global WhatsApp client instance
whatsapp_client = WhatsAppClient()
