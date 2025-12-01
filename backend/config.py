"""
Configuration management for the WhatsApp AI Sales Agent backend.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenRouter AI
    openrouter_api_key: str
    
    # Supabase
    supabase_project_ref: str
    supabase_service_key: str
    supabase_url: str
    
    # Twilio WhatsApp API
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_whatsapp_number: str  # Format: whatsapp:+14155238886
    
    # Application
    port: int = 8000
    environment: str = "development"
    log_level: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Global settings instance
settings = Settings()
