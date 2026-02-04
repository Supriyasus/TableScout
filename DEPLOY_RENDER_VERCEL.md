# Deploy TableScout on Render + Vercel (No Docker Required)

This guide covers deploying your TableScout app without Docker:
- **Frontend**: Vercel (hosting React app)
- **Backend**: Render (hosting FastAPI API)
- **Database**: PostgreSQL on Render

---

## Prerequisites

1. **GitHub Account** (required for both Render and Vercel)
2. **Render Account** ([Sign up free](https://render.com))
3. **Vercel Account** ([Sign up free](https://vercel.com))
4. **Git** installed locally

---

## Step 1: Prepare Your Repository

### 1.1 Push Code to GitHub

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit"

# Add GitHub remote and push
git remote add origin https://github.com/YOUR_USERNAME/TableScout.git
git branch -M main
git push -u origin main
```

### 1.2 Create `.env` Files

Create these files in your project root (they should NOT be committed):

**`.env.local`** (for local development):
```env
REACT_APP_API_URL=http://localhost:8000/api
```

---

## Step 2: Deploy Backend to Render

### 2.1 Create PostgreSQL Database on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `tablescout-db`
   - **Database**: `tablescout`
   - **User**: `postgres`
   - **Region**: Choose closest to you
   - **Plan**: Free (or Starter Paid)
4. Click **"Create Database"**
5. Copy the **Internal Database URL** (looks like: `postgresql://user:password@dpg-xxx.internal/tablescout`)

### 2.2 Create Web Service for Backend

1. In Render Dashboard, click **"New +"** → **"Web Service"**
2. Select **"Connect a repository"** and authorize GitHub
3. Select your `TableScout` repository
4. Configure:
   - **Name**: `tablescout-backend`
   - **Runtime**: `Python 3.11`
   - **Build Command**: `pip install -r backend/requirements.txt && pip install gunicorn`
   - **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app --bind 0.0.0.0:10000`
   - **Plan**: Free (or Starter Paid)
5. Click **"Advanced"** and add **Environment Variables**:

   | Key | Value |
   |-----|-------|
   | `DATABASE_URL` | (Paste the Internal URL from step 2.1) |
   | `SECRET_KEY` | Generate: `openssl rand -hex 32` |
   | `GEMINI_API_KEY` | Your actual Gemini API key |
   | `ENVIRONMENT` | `production` |
   | `FRONTEND_URL` | (Leave blank for now, update after Vercel deployment) |
   | `PYTHON_VERSION` | `3.11` |

6. Click **"Create Web Service"**
7. Wait for deployment (~2-3 minutes)
8. Copy your backend URL (e.g., `https://tablescout-backend.onrender.com`)

### 2.3 Update Backend CORS

Edit [backend/main.py](backend/main.py) and update `allow_origins`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",        # Local development
        "http://localhost",              # Local Docker
        "https://tablescout.vercel.app", # Your Vercel domain (update this)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push:
```bash
git add backend/main.py
git commit -m "Update CORS for Vercel deployment"
git push
```

---

## Step 3: Deploy Frontend to Vercel

### 3.1 Connect Repository to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Select your GitHub repository
4. Configure:
   - **Framework Preset**: `Create React App`
   - **Root Directory**: `frontend` (important!)
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
5. Click **"Advanced"** and add **Environment Variables**:

   | Key | Value |
   |-----|-------|
   | `REACT_APP_API_URL` | `https://tablescout-backend.onrender.com/api` |

6. Click **"Deploy"**
7. Wait for deployment (~2-3 minutes)
8. Your app is live at: `https://YOUR_PROJECT_NAME.vercel.app`

### 3.2 Custom Domain (Optional)

In Vercel Dashboard:
1. Go to **Settings** → **Domains**
2. Add your custom domain
3. Follow DNS configuration steps

---

## Step 4: Update Backend CORS with Vercel URL

After Vercel deployment, update [backend/main.py](backend/main.py) with your actual Vercel URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://YOUR_PROJECT_NAME.vercel.app",  # Your actual Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Push the change:
```bash
git add backend/main.py
git commit -m "Update CORS with production Vercel URL"
git push
```

Render will auto-redeploy with the updated CORS settings.

---

## Deployment Flow Diagram

```
Your GitHub Repository
    ↓
    ├─→ Render (watches for changes)
    │   ├─ Pulls latest code
    │   ├─ Installs Python dependencies
    │   ├─ Starts Gunicorn server
    │   └─ Connected to PostgreSQL database
    │
    └─→ Vercel (watches for changes)
        ├─ Pulls latest code
        ├─ Runs: npm run build (in frontend/)
        ├─ Optimizes React app
        └─ Deploys to CDN (worldwide)
```

---

## Environment Variables Summary

### Backend (Render)
```env
DATABASE_URL=postgresql://user:password@host:port/tablescout
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
ENVIRONMENT=production
FRONTEND_URL=https://yourapp.vercel.app
PYTHON_VERSION=3.11
```

### Frontend (Vercel)
```env
REACT_APP_API_URL=https://tablescout-backend.onrender.com/api
```

---

## How It Works

### 1. **Automatic Deployment on Git Push**
```bash
git commit -m "Fix bug"
git push origin main
```
↓
→ Render detects change, rebuilds backend
→ Vercel detects change, rebuilds frontend
→ Both live within 2-5 minutes

### 2. **Database Persistence**
- PostgreSQL on Render is persistent
- Data survives application restarts
- Render provides automated backups (on paid plans)

### 3. **Scaling**
- **Vercel**: Automatically scales globally with CDN
- **Render**: Scale by upgrading plan
- **Database**: Upgrade PostgreSQL plan as needed

---

## Testing Your Deployment

### 1. Test Backend Health
```bash
curl https://tablescout-backend.onrender.com/health
```

Expected response:
```json
{"status": "ok", "db": "connected"}
```

### 2. Test Frontend
Visit: `https://YOUR_PROJECT.vercel.app`

### 3. Test API Connection
- Open your app
- Search for a place
- Check browser DevTools (F12 → Network tab)
- Verify requests go to your Render backend

---

## Troubleshooting

### Backend won't deploy
**Problem**: Build fails
- Check logs: Render Dashboard → Select service → Logs
- Verify all dependencies in `backend/requirements.txt`
- Ensure `SECRET_KEY` and `GEMINI_API_KEY` are set

### Database connection error
```
Error: could not connect to database
```
**Solutions**:
1. Verify `DATABASE_URL` is correct (internal URL, not external)
2. Wait 30 seconds after database creation (not immediately ready)
3. Check PostgreSQL status in Render Dashboard

### CORS errors in browser
```
Access to XMLHttpRequest has been blocked by CORS policy
```
**Solution**:
1. Add your Vercel URL to `allow_origins` in [backend/main.py](backend/main.py)
2. Commit and push
3. Wait for Render to redeploy

### Frontend environment variables not working
**Problem**: `REACT_APP_API_URL` shows as `undefined`
**Solution**:
1. Vercel requires `REACT_APP_` prefix for frontend variables
2. Verify it's set in Vercel Dashboard → Settings → Environment Variables
3. Redeploy: Go to Deployments → Select latest → Click "Redeploy"

### App is very slow / takes 30 seconds to wake up
**Reason**: Free tier services sleep after inactivity
**Solutions**:
1. Upgrade to paid plans (Vercel Hobby $5/month, Render $7/month)
2. Or use [UptimeRobot](https://uptimerobot.com) (free) to ping backend every 5 minutes

---

## File Structure Reminder

```
TableScout/
├── frontend/
│   ├── package.json
│   ├── src/
│   │   └── api.js (ensure this points to REACT_APP_API_URL)
│   └── ... other React files
├── backend/
│   ├── main.py (update CORS here)
│   ├── requirements.txt
│   ├── api/
│   ├── agents/
│   └── ... other Python files
├── vercel.json (used by Vercel)
├── render.yaml (reference only, uses dashboard)
└── README.md
```

---

## Pricing

### Free Tier (Perfect for Testing)
- **Vercel**: Unlimited projects, 100 GB bandwidth/month
- **Render**: 750 compute hours/month (free tier, sleeps after inactivity)
- **PostgreSQL**: Shared free tier (limited)

### Paid Tier (Recommended for Production)
- **Vercel Hobby**: $5/month per project
- **Render Starter**: $7/month (no sleep, better performance)
- **PostgreSQL Starter**: $12/month (dedicated instance)

**Total**: ~$24/month for a production-grade setup

---

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Create PostgreSQL database on Render
3. ✅ Deploy backend to Render
4. ✅ Deploy frontend to Vercel
5. ✅ Test the full app
6. ✅ Set custom domain (optional)
7. ✅ Monitor for errors in dashboards
8. ✅ Set up alerts (optional)

---

## Useful Commands

```bash
# View deployment logs
# Render: Dashboard → Select service → Logs
# Vercel: Dashboard → Deployments → Click deployment → Logs

# Force redeploy without code changes
# Render: Dashboard → Select service → Manual Deploy
# Vercel: Dashboard → Deployments → Redeploy

# Rollback to previous version
# Render: Automatic on failed deployment
# Vercel: Deployments → Click older version → Promote to Production
```

---

## Security Checklist

- [ ] `SECRET_KEY` is strong (use `openssl rand -hex 32`)
- [ ] Environment variables are set in dashboards (not in code)
- [ ] `.env` files are in `.gitignore`
- [ ] CORS origins are restricted (not `*`)
- [ ] Database password is strong
- [ ] API keys (Gemini) are not committed to GitHub
- [ ] HTTPS is enabled (automatic on both platforms)

---

## Support Resources

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/
- **React Production Build**: https://create-react-app.dev/docs/deployment/

---

**Congratulations!** Your app is now deployed and live on the internet! 🎉
