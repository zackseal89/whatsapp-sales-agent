import asyncio
from supabase import create_client, Client
from config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_admin_user():
    """Create a test admin user."""
    try:
        # Initialize Supabase client with SERVICE ROLE key (admin access)
        supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_key
        )
        
        email = "admin@example.com"
        password = "password123"
        
        logger.info(f"Attempting to create user: {email}")
        
        # Create user using admin auth API
        user = supabase.auth.admin.create_user({
            "email": email,
            "password": password,
            "email_confirm": True,
            "user_metadata": {"name": "Admin User", "role": "admin"}
        })
        
        logger.info("✅ User created successfully!")
        logger.info(f"ID: {user.user.id}")
        logger.info(f"Email: {user.user.email}")
        
        # Also insert into public.admin_users table if needed
        # (Our schema has an admin_users table, let's sync it)
        try:
            supabase.table("admin_users").insert({
                "id": user.user.id,
                "email": email,
                "name": "Admin User",
                "role": "admin"
            }).execute()
            logger.info("✅ Added to public.admin_users table")
        except Exception as e:
            logger.warning(f"Could not add to admin_users table (might already exist): {e}")

    except Exception as e:
        logger.error(f"❌ Failed to create user: {e}")

if __name__ == "__main__":
    asyncio.run(create_admin_user())
