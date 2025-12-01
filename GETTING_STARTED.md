# Getting Started - WhatsApp AI Sales Agent

This guide will help you set up and run the WhatsApp AI Sales Agent project locally.

## Prerequisites

- **Python 3.11+** - For the backend AI agent
- **Node.js 18+** - For the Next.js dashboard
- **pnpm** - Package manager for frontend
- **Supabase Account** - Database and authentication
- **Google Cloud Account** - For Gemini API
- **WhatsApp Business Account** - For messaging API

## Quick Start

### 1. Clone and Navigate to Project

```bash
cd "C:\Users\user\OneDrive\Desktop\Whatsapp sales agent"
```

### 2. Set Up Supabase Database

1. Create a new project at [supabase.com](https://supabase.com)
2. Copy your project reference ID and service role key
3. In the SQL Editor, run the schema:
   ```sql
   -- Copy and paste contents of database/schema.sql
   ```
4. (Optional) Load seed data:
   ```sql
   -- Copy and paste contents of database/seed.sql
   ```

### 3. Set Up Backend (Python AI Agent)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env

# Edit .env and fill in your credentials:
# - GOOGLE_API_KEY (from Google Cloud Console)
# - SUPABASE_PROJECT_REF
# - SUPABASE_SERVICE_KEY  
# - WHATSAPP_TOKEN (from Meta Business)
# - WHATSAPP_PHONE_NUMBER_ID
# - WEBHOOK_VERIFY_TOKEN (create a random string)
```

### 4. Set Up Frontend (Next.js Dashboard)

```bash
cd ../frontend

# Install dependencies
pnpm install

# Create environment file
copy .env.example .env.local

# Edit .env.local and fill in:
# - NEXT_PUBLIC_SUPABASE_URL
# - NEXT_PUBLIC_SUPABASE_ANON_KEY
# - SUPABASE_SERVICE_ROLE_KEY
```

### 5. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Activate virtual environment
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
pnpm dev
```

**Access Points:**
- Dashboard: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Environment Setup Details

### Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy to `backend/.env` as `GOOGLE_API_KEY`

### Supabase Configuration

1. Project Settings → API
2. Copy **Project URL** → `NEXT_PUBLIC_SUPABASE_URL`
3. Copy **anon/public key** → `NEXT_PUBLIC_SUPABASE_ANON_KEY`
4. Copy **service_role key** → `SUPABASE_SERVICE_KEY` (backend) and `SUPABASE_SERVICE_ROLE_KEY` (frontend)
5. Project Settings → General → Reference ID → `SUPABASE_PROJECT_REF`

### WhatsApp Business API

1. Create a Meta Business account
2. Set up WhatsApp Business API (Cloud API)
3. Get your Access Token → `WHATSAPP_TOKEN`
4. Get Phone Number ID → `WHATSAPP_PHONE_NUMBER_ID`
5. Configure webhook URL: `https://your-domain.com/webhooks/whatsapp`
6. Set verify token (match with `WEBHOOK_VERIFY_TOKEN`)

## Next Steps

1. **Configure AI Agents**: Edit prompts in `backend/agents/`
2. **Customize Dashboard**: Modify UI in `frontend/app/`
3. **Add Products**: Use dashboard or run seed data
4. **Test Conversations**: Send WhatsApp message to your business number

## Troubleshooting

### Backend won't start
- Ensure Python 3.11+ is installed
- Check all environment variables are set in `.env`
- Verify virtual environment is activated

### Frontend build errors
- Run `pnpm install` again
- Clear `.next` folder and rebuild
- Check Node.js version (18+)

### WhatsApp webhook not receiving messages
- Ensure webhook URL is publicly accessible (use ngrok for local testing)
- Verify `WEBHOOK_VERIFY_TOKEN` matches in Meta dashboard
- Check WhatsApp Business API subscription status

## Development Workflow

1. Make changes to code
2. Both servers auto-reload (backend with `--reload`, frontend with Vite HMR)
3. Test locally
4. Commit to git
5. Deploy (see DEPLOYMENT.md)

## Documentation

- [Product Requirements Document](./docs/PRD.md)
- [API Documentation](./backend/README.md)
- [Database Schema](./database/schema.sql)
- [Deployment Guide](./docs/DEPLOYMENT.md)

## Support

For issues or questions, refer to:
- [Google ADK Docs](https://google.github.io/adk-docs/)
- [Supabase Docs](https://supabase.com/docs)
- [WhatsApp API Docs](https://developers.facebook.com/docs/whatsapp)
