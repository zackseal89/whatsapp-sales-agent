# Deployment Guide

This guide walks you through deploying the WhatsApp AI Sales Agent to production.

## Prerequisites

- GitHub account
- Vercel account (free tier works)
- Supabase project (configured)
- Twilio WhatsApp Business account
- OpenRouter API key

---

## Part 1: Push to GitHub

### Step 1: Create a New GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Create a new repository (e.g., `whatsapp-sales-agent`)
3. **Do NOT** initialize with README (we already have one)
4. Set visibility (Public or Private)

### Step 2: Link Local Repository to GitHub

Open your terminal in the project root directory and run:

```bash
# Check git status (should already be initialized)
git status

# Add all files to staging
git add .

# Commit the changes
git commit -m "Initial commit: WhatsApp AI Sales Agent"

# Add your GitHub repository as remote origin
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Verify Push

Visit your GitHub repository URL to confirm all files were pushed correctly.

> [!IMPORTANT]
> Verify that `.env` files are NOT visible in your GitHub repository. Only `.env.example` files should be present.

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Import Project to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Vercel will auto-detect Next.js configuration

### Step 2: Configure Build Settings

**Root Directory**: `frontend`

Vercel should auto-detect:
- **Framework Preset**: Next.js
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

### Step 3: Configure Environment Variables

Add the following environment variables in Vercel:

| Variable Name | Value | Where to Get It |
|--------------|-------|-----------------|
| `NEXT_PUBLIC_SUPABASE_URL` | `https://your-project.supabase.co` | Supabase Dashboard → Settings → API |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Your anon/public key | Supabase Dashboard → Settings → API |
| `SUPABASE_SERVICE_ROLE_KEY` | Your service role key | Supabase Dashboard → Settings → API (keep secret!) |

> [!WARNING]
> The `SUPABASE_SERVICE_ROLE_KEY` has admin privileges. Never expose it in client-side code.

### Step 4: Deploy

1. Click **"Deploy"**
2. Wait for build to complete (~2-3 minutes)
3. Vercel will provide a URL (e.g., `your-app.vercel.app`)

### Step 5: Test Deployment

1. Visit your Vercel URL
2. Verify the dashboard loads correctly
3. Test authentication flow
4. Check that conversations and orders display properly

---

## Part 3: Backend Deployment (Optional)

The backend currently runs locally and uses `ngrok` for webhooks. For production, consider:

### Option A: Keep Using ngrok (Development/Testing)
- Simple and free
- Good for testing and low-traffic scenarios
- Requires keeping your local server running

### Option B: Deploy to Production (Recommended for Production)

Deploy your backend to:
- **Railway.app** (Easy, automatic deployments)
- **Fly.io** (Good for Python apps)
- **Google Cloud Run** (Scalable, pay-per-use)
- **AWS Lambda** (Serverless)

**Environment Variables Needed for Backend:**
```bash
OPENROUTER_API_KEY=your_key
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_service_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
PORT=8000
ENVIRONMENT=production
LOG_LEVEL=INFO
```

---

## Part 4: Configure Twilio Webhook

Once your backend is deployed (or running via ngrok):

1. Go to [Twilio Console](https://console.twilio.com/)
2. Navigate to **Messaging** → **Settings** → **WhatsApp Sandbox Settings**
3. Set **"When a message comes in"** to:
   ```
   https://your-backend-url.com/webhooks/whatsapp
   ```
4. HTTP Method: `POST`
5. Save configuration

Test by sending a WhatsApp message to your Twilio number.

---

## Part 5: Update CORS for Production (Backend)

If deploying frontend and backend separately, update `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-app.vercel.app",  # Your Vercel URL
        "http://localhost:3000"  # Keep for local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Troubleshooting

### Frontend Build Fails on Vercel

**Issue**: Build fails with module errors

**Solution**:
1. Ensure `package.json` is in the `frontend/` directory
2. Verify Root Directory is set to `frontend` in Vercel settings
3. Check that all dependencies are listed in `package.json`

### Environment Variables Not Working

**Issue**: App can't connect to Supabase

**Solution**:
1. Verify environment variable names match exactly (case-sensitive)
2. Redeploy after adding/changing environment variables
3. Check for trailing spaces in values

### WhatsApp Messages Not Received

**Issue**: Backend doesn't receive webhooks

**Solution**:
1. Verify webhook URL in Twilio console
2. Check that backend is running and accessible
3. Review backend logs for errors
4. Test webhook with Twilio's webhook tester

### CORS Errors in Browser

**Issue**: Frontend can't connect to backend

**Solution**:
1. Update `allow_origins` in `backend/main.py` to include your Vercel URL
2. Ensure credentials are enabled
3. Redeploy backend after changes

---

## Monitoring & Maintenance

### Vercel Deployment
- Check deployment logs: Vercel Dashboard → Your Project → Deployments
- Monitor analytics: Vercel Dashboard → Analytics
- View function logs: Vercel Dashboard → Your Project → Functions

### Backend Monitoring
- Check application logs regularly
- Monitor Twilio usage and costs
- Review OpenRouter API usage
- Monitor Supabase database size

### Database Maintenance
- Set up Supabase backups (automatic on paid plans)
- Review RLS policies regularly
- Monitor storage usage

---

## Security Checklist

- [x] `.env` files are in `.gitignore`
- [ ] All API keys are stored in environment variables
- [ ] CORS is configured for specific origins (not `*`)
- [ ] Supabase RLS policies are enabled
- [ ] Service role keys are never exposed to frontend
- [ ] Webhook endpoints validate requests (consider adding Twilio signature validation)

---

## Next Steps

1. **Set up monitoring** - Use Vercel Analytics and Supabase logs
2. **Configure custom domain** - Add your domain in Vercel settings
3. **Enable HTTPS** - Vercel provides SSL certificates automatically
4. **Set up CI/CD** - Vercel auto-deploys on `git push` to main branch
5. **Scale as needed** - Monitor usage and upgrade plans if necessary

---

## Support Resources

- **Vercel Documentation**: https://vercel.com/docs
- **Next.js Documentation**: https://nextjs.org/docs
- **Supabase Documentation**: https://supabase.com/docs
- **Twilio Documentation**: https://www.twilio.com/docs/whatsapp
- **OpenRouter Documentation**: https://openrouter.ai/docs

---

## Cost Estimation

### Free Tier Limits
- **Vercel**: 100GB bandwidth, unlimited projects
- **Supabase**: 500MB database, 2GB bandwidth
- **Twilio**: Pay-per-message (~$0.005 per message)
- **OpenRouter**: Pay-per-token (varies by model)

Monitor usage to stay within free tiers or plan for scaling costs.
