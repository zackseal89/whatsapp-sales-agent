# WhatsApp AI Sales Agent

An AI-powered WhatsApp sales agent built with OpenRouter AI, Supabase, and Next.js. Features intelligent conversation handling, automated order collection, and real-time notifications.

## ✨ Features

- **AI-Powered Conversations**: Natural language interactions powered by Grok-2 via OpenRouter
- **Manual Payment Flow**: AI agent collects order details without processing payments
- **Real-Time Notifications**: Store owners receive instant notifications when orders are placed
- **Customer Management**: Track all customer interactions and conversation history
- **Product Catalog**: Manage products via dashboard
- **Order Tracking**: Monitor all orders with status updates

## Project Structure

```
├── backend/              # Python AI Agent (FastAPI)
├── frontend/             # Next.js Dashboard
└── README.md
```

## Tech Stack

### Backend (AI Agent)
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **LLM**: Grok-2 (via OpenRouter API)
- **Database**: Supabase
- **Messaging**: Twilio WhatsApp API

### Frontend (Dashboard)
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **Database**: Supabase
- **Real-time**: Supabase Realtime subscriptions

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Supabase account
- Twilio account with WhatsApp sandbox
- OpenRouter API key

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create `.env` file (see `.env.example`):
```
OPENROUTER_API_KEY=your_openrouter_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_service_key
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
PORT=8000
ENVIRONMENT=development
```

4. Run the server:
```bash
python main.py
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file:
```
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

4. Run the development server:
```bash
npm run dev
```

### Exposing Backend via Ngrok

To receive WhatsApp webhooks, expose your local backend:
```bash
ngrok http 8000
```

Configure your Twilio webhook URL to:
```
https://your-ngrok-url.ngrok-free.app/webhooks/whatsapp
```

## Manual Payment Flow

The AI agent is configured to act as an "Order Taker" that:

1. **Collects order details** through natural conversation
2. **Does NOT request payment** information
3. **Saves orders** to database with `pending_payment` status
4. **Notifies store owner** in real-time via dashboard
5. **Tells customer** the store owner will contact them for payment

When a customer confirms an order, the agent:
- Extracts items and quantities
- Generates an order number
- Stores in Supabase `orders` table
- Triggers real-time notification on dashboard

## Database Schema

Required Supabase tables:
- `customers` - Customer records
- `conversations` - Chat sessions
- `messages` - Individual messages
- `orders` - Order records with pending_payment status
- `products` - Product catalog

See `backend/services/supabase.py` for schema details.

## License

MIT

