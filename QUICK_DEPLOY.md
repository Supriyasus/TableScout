# Quick Deploy Guide: Render + Vercel

## TL;DR - 5 Minute Setup

### 1. Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Create PostgreSQL on Render
- [Render Dashboard](https://render.com) → **New +** → **PostgreSQL**
- Name: `tablescout-db`
- Copy the **Internal Database URL**

### 3. Deploy Backend
- Render Dashboard → **New +** → **Web Service**
- Connect your GitHub repo
- **Runtime**: Python 3.11
- **Build Command**: `pip install -r backend/requirements.txt && pip install gunicorn`
- **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app --bind 0.0.0.0:10000`
- **Environment Variables**:
  ```
  DATABASE_URL=<paste your internal URL>
  SECRET_KEY=<run: openssl rand -hex 32>
  GEMINI_API_KEY=<your API key>
  ENVIRONMENT=production
  PYTHON_VERSION=3.11
  ```
- Deploy & copy your backend URL (e.g., `https://tablescout-backend.onrender.com`)

### 4. Deploy Frontend
- [Vercel Dashboard](https://vercel.com) → **Add New** → **Project**
- Select your GitHub repo
- **Root Directory**: `frontend`
- **Framework**: Create React App
- **Environment Variables**:
  ```
  REACT_APP_API_URL=https://tablescout-backend.onrender.com/api
  ```
- Deploy & you're done!

### 5. Update CORS (Backend)
Edit `backend/main.py` - update `allow_origins`:
```python
allow_origins=[
    "http://localhost:3000",
    "https://YOUR_VERCEL_URL.vercel.app",  # Your actual Vercel domain
],
```
Push to GitHub → Render auto-redeploys

## What Gets Deployed?

| Component | Platform | What Happens |
|-----------|----------|--------------|
| **React Frontend** | Vercel | Auto-builds with `npm run build`, serves globally |
| **FastAPI Backend** | Render | Installs Python deps, runs Gunicorn server |
| **PostgreSQL DB** | Render | Managed database, data persists |

## Auto-Redeploy on Git Push?

Yes! Both Render and Vercel watch your GitHub repo:
```bash
git push origin main
↓
✅ Render detects change → rebuilds backend
✅ Vercel detects change → rebuilds frontend
↓
Changes live in 2-5 minutes
```

## Test It
```bash
curl https://tablescout-backend.onrender.com/health
# Should return: {"status": "ok", "db": "connected"}
```

## Costs
- **Free tier**: Works but backend sleeps after 15 min inactivity
- **Upgrade**: Render Starter ($7/mo) + Vercel ($5/mo) = ~$12/mo production-ready

See [DEPLOY_RENDER_VERCEL.md](DEPLOY_RENDER_VERCEL.md) for detailed steps!
