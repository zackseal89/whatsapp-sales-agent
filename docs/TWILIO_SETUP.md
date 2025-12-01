# Twilio WhatsApp Setup Guide

This guide will help you set up Twilio WhatsApp API for the sales agent.

## Prerequisites

- Twilio account (sign up for free trial at [twilio.com](https://www.twilio.com/try-twilio))
- Phone number capable of receiving WhatsApp messages

## Quick Setup (Sandbox Mode - Recommended for Development)

### Step 1: Create Twilio Account

1. Go to [https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio)
2. Sign up for a free account
3. Verify your email and phone number

### Step 2: Access WhatsApp Sandbox

1. Log into Twilio Console
2. Navigate to **Messaging** → **Try it out** → **Send a WhatsApp message**
3. You'll see the sandbox number and join code (e.g., `join word-word`)

### Step 3: Join the Sandbox

1. Open WhatsApp on your phone
2. Send a message to the Twilio sandbox number shown (usually starts with +1 415)
3. Send the join code exactly as shown (e.g., `join cosmic-winter`)
4. You'll receive a confirmation message

### Step 4: Get Your Credentials

1. In Twilio Console, go to **Account** → **Dashboard**
2. Copy your **Account SID** and **Auth Token**
3. Note your **WhatsApp Sandbox Number** (from Messaging → Try WhatsApp)

### Step 5: Configure Backend

1. Open `backend/.env` (create from `.env.example` if needed)
2. Add your Twilio credentials:

```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886  # Your sandbox number
```

### Step 6: Set Up Webhook

1. In Twilio Console, go to **Messaging** → **Try it out** → **Send a WhatsApp message**
2. Scroll to **Sandbox Configuration**
3. In **WHEN A MESSAGE COMES IN**, enter your webhook URL:
   ```
   https://your-domain.com/webhooks/whatsapp
   ```
   
   **For local development with ngrok:**
   ```bash
   # Install ngrok: https://ngrok.com/download
   ngrok http 8000
   
   # Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
   # Webhook URL: https://abc123.ngrok.io/webhooks/whatsapp
   ```

4. Set HTTP method to **POST**
5. Click **Save**

### Step 7: Test the Integration

1. Start your backend server:
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Mac/Linux
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```

2. Send a test message to the Twilio WhatsApp number
3. You should receive an echo response!

## Production Setup (WhatsApp Business Account)

For production use, you'll need to upgrade to a full WhatsApp Business Account:

### Requirements

- Business verification
- Facebook Business Manager account
- Approved business use case
- WhatsApp Business Profile

### Steps

1. **Request Access**:
   - Go to Twilio Console → Messaging → Senders → WhatsApp senders
   - Click "Request to enable my Twilio numbers for WhatsApp"
   - Fill out the business verification form

2. **Business Verification**:
   - Provide business details
   - Submit required documents
   - Wait for Meta approval (can take 1-2 weeks)

3. **Get WhatsApp Number**:
   - Purchase a Twilio phone number
   - Enable WhatsApp on that number
   - Configure business profile

4. **Update Credentials**:
   ```bash
   TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890  # Your approved number
   ```

## Pricing

### Sandbox (Free)
- ✅ Unlimited incoming messages
- ✅ Up to 500 outgoing messages (free trial credits)
- ⚠️ Users must join sandbox first

### Production
- **Conversation-based pricing**:
  - ~$0.005 per conversation (varies by country)
  - Conversation = 24-hour window after your first reply
- **Session messages**:
  - Free within 24-hour conversation window
- **Template messages**:
  - Used outside 24-hour window
  - ~$0.02-$0.04 per message

[Full pricing details](https://www.twilio.com/en-us/whatsapp/pricing)

## Troubleshooting

### Webhook not receiving messages

1. **Check webhook URL is correct**
   - Should be HTTPS (required by Twilio)
   - Should be publicly accessible
   - For local dev, use ngrok

2. **Verify sandbox join**
   - Send the join code to sandbox number
   - Check you received confirmation

3. **Check server logs**
   ```bash
   # Should see: "Received message from whatsapp:+..."
   ```

### Messages not sending

1. **Check Twilio credentials**
   - Account SID and Auth Token correct
   - No typos in .env file

2. **Check phone number format**
   - Should be: `whatsapp:+1234567890`
   - Include country code

3. **Check Twilio logs**
   - Go to Twilio Console → Monitor → Logs → Errors
   - Look for error details

### "User is not a valid WhatsApp user"

- User hasn't joined sandbox
- Send join code first before sending messages

## Useful Links

- [Twilio WhatsApp Quickstart](https://www.twilio.com/docs/whatsapp/quickstart/python)
- [WhatsApp Sandbox Tutorial](https://www.twilio.com/docs/whatsapp/sandbox)
- [Twilio Console](https://console.twilio.com/)
- [Error Codes Reference](https://www.twilio.com/docs/api/errors)

## Next Steps

Once your Twilio integration is working:

1. ✅ Test basic message send/receive
2. 🔄 Implement AI agent integration (Phase 2 - Week 3)
3. 🔄 Add product search capabilities
4. 🔄 Build order processing
5. 🚀 Deploy to production

---

**Need help?** Check the [Twilio Community](https://www.twilio.com/community) or [support docs](https://support.twilio.com/).
