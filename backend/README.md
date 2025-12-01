# Quick Start - Running the Backend

## Prerequisites

- Python 3.11+
- Twilio account (free trial works)
- ngrok (for local webhook testing)

## Setup Steps

### 1. Install Dependencies

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy template
copy .env.example .env

# Edit .env with your credentials:
# - GOOGLE_API_KEY (from https://makersuite.google.com/app/apikey)
# - SUPABASE_PROJECT_REF, SUPABASE_SERVICE_KEY, SUPABASE_URL
# - TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER
```

### 3. Set Up Twilio Sandbox

See [docs/TWILIO_SETUP.md](../docs/TWILIO_SETUP.md) for detailed instructions.

**Quick version:**
1. Go to Twilio Console → Messaging → Try WhatsApp
2. Note your sandbox number
3. Join sandbox from your phone
4. Configure webhook URL

### 4. Run the Server

```bash
uvicorn main:app --reload --port 8000
```

Server will start at `http://localhost:8000`

### 5. Expose with ngrok (for webhooks)

```bash
# In a new terminal
ngrok http 8000

# Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
# Set as webhook in Twilio: https://abc123.ngrok.io/webhooks/whatsapp
```

### 6. Test

1. Send a message to your Twilio WhatsApp sandbox number
2. You should receive an echo response
3. Check logs in your terminal

## API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /webhooks/whatsapp` - Twilio webhook handler

## Troubleshooting

**Server won't start:**
- Check Python version: `python --version` (should be 3.11+)
- Ensure virtual environment is activated
- Verify all env variables are set

**Webhook not receiving messages:**
- Check ngrok is running
- Verify webhook URL in Twilio Console
- Check you joined the sandbox

**Dependencies errors:**
- Try: `pip install --upgrade pip`
- Then: `pip install -r requirements.txt --force-reinstall`

## Next Steps

Phase 2 implementation:
1. ✅ Twilio integration (DONE)
2. ⏳ Google ADK Router Agent
3. ⏳ Product Search Agent with Supabase MCP
4. ⏳ Full conversation flow

See [../docs/PHASE_2_PLAN.md](../docs/PHASE_2_PLAN.md) for details.
