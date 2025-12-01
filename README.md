# WhatsApp AI Sales Agent

An AI-powered WhatsApp sales agent built with Google ADK, Supabase, and Next.js.

## Project Structure

```
├── backend/              # Python AI Agent (Google ADK)
├── frontend/             # Next.js Dashboard
├── database/             # Supabase SQL migrations
├── docs/                 # Documentation
└── README.md
```

## Tech Stack

### Backend (AI Agent)
- **Framework**: Google Agent Development Kit (ADK)
- **Language**: Python 3.11+
- **LLM**: Gemini Pro
- **Database**: Supabase (via MCP)
- **API**: Twilio WhatsApp API

### Frontend (Dashboard)
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **Database**: Supabase
- **Deployment**: Vercel

## Getting Started

See individual README files in `backend/` and `frontend/` directories for setup instructions.

## Development Phases

1. **Phase 1**: Foundation (Weeks 1-2) - Project setup, database schema
2. **Phase 2**: Core AI Agent (Weeks 3-4) - Basic conversation flow
3. **Phase 3**: Specialized Agents (Weeks 5-6) - Product search, orders, support
4. **Phase 4**: Dashboard Features (Weeks 7-8) - Admin interface
5. **Phase 5**: Testing & Refinement (Weeks 9-10) - QA and optimization
6. **Phase 6**: Launch Preparation (Weeks 11-12) - Production deployment

## Documentation

- [Product Requirements Document](./docs/PRD.md)
- [Database Schema](./database/schema.sql)
- [API Documentation](./docs/API.md)

## Environment Variables

### Backend
```
GOOGLE_API_KEY=your_gemini_api_key
SUPABASE_PROJECT_REF=your_project_ref
SUPABASE_SERVICE_KEY=your_service_key
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### Frontend
```
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

## License

MIT
