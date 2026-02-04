# TableScout Deployment Guide

## Overview
This guide covers building and deploying the TableScout application (Frontend React + Backend FastAPI + PostgreSQL Database).

---

## Pre-Deployment Setup

### 1. Environment Configuration
Create a `.env` file in the root directory with production values:

```bash
cp .env.example .env
```

Update `.env` with your production credentials:
```env
DATABASE_URL=postgresql://user:password@your-host:5432/tablescout
SECRET_KEY=generate-a-strong-secret-key-here
GEMINI_API_KEY=your-actual-gemini-api-key
FRONTEND_URL=https://your-domain.com
ENVIRONMENT=production
```

---

## Option 1: Local Development Build

### Frontend Build
```bash
cd frontend
npm install
npm run build
```
Output: `frontend/build/` directory (ready for serving)

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Backend runs on: `http://localhost:8000`

---

## Option 2: Docker Deployment (Recommended)

### Prerequisites
- Docker installed ([Download](https://www.docker.com/products/docker-desktop))
- Docker Compose installed (included with Docker Desktop)

### 1. Build and Run with Docker Compose

```bash
# From project root directory
docker-compose up --build
```

This starts:
- **PostgreSQL** on `localhost:5432`
- **Backend API** on `localhost:8000`
- **Frontend** on `localhost`

### 2. Initialize Database

```bash
# Run migrations (if you have them)
docker exec tablescout-backend python backend/db/init_db.py
```

### 3. Stop Services

```bash
docker-compose down
```

### 4. View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

---

## Option 3: Cloud Deployment (AWS, GCP, Azure, etc.)

### Using AWS ECS (Example)

#### 1. Build and Push Docker Images
```bash
# Login to AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build backend
docker build -f Dockerfile.backend -t tablescout-backend:latest .
docker tag tablescout-backend:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/tablescout-backend:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/tablescout-backend:latest

# Build frontend
docker build -f Dockerfile.frontend -t tablescout-frontend:latest .
docker tag tablescout-frontend:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/tablescout-frontend:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/tablescout-frontend:latest
```

#### 2. Create ECS Task Definition
Use the docker-compose.yml as reference to create an ECS task definition with:
- Database container (RDS for production)
- Backend container
- Frontend container

#### 3. Create ECS Service and Scale

### Using Render.com (Simpler Alternative)

1. Push code to GitHub
2. Connect GitHub repo to Render
3. Create services:
   - PostgreSQL database (managed)
   - Backend web service
   - Frontend static site
4. Set environment variables
5. Auto-deploys on git push

### Using Heroku (Deprecated but still available)

```bash
# Install Heroku CLI
npm install -g heroku

# Login
heroku login

# Create app
heroku create tablescout-backend
heroku create tablescout-frontend

# Set environment variables
heroku config:set DATABASE_URL=postgresql://...
heroku config:set GEMINI_API_KEY=...

# Deploy backend
git subtree push --prefix backend heroku main

# Deploy frontend
git subtree push --prefix frontend heroku main
```

---

## Build Process Explained

### Frontend Build (`npm run build`)
```
Source Code (React)
    ↓
Webpack (Module bundler)
    ↓
Babel (JS transpilation)
    ↓
Minification & Optimization
    ↓
build/ folder (Production-ready static files)
    ↓
Served by Nginx/Web Server
```

**Output includes:**
- Minified JavaScript
- Optimized CSS
- Compressed images
- Source maps (for debugging)

### Backend Build (Docker)
```
Python Source Code
    ↓
pip install dependencies
    ↓
Docker image created
    ↓
Gunicorn WSGI server (production)
    ↓
Runs on port 8000
```

---

## Deployment Checklist

- [ ] Update `.env` with production credentials
- [ ] Set strong `SECRET_KEY`
- [ ] Update `CORS` origins in `backend/main.py`
- [ ] Update database connection string
- [ ] Test locally with `docker-compose`
- [ ] Verify health endpoints: `/health`
- [ ] Test API endpoints
- [ ] Verify frontend can reach backend
- [ ] Set up SSL/HTTPS
- [ ] Enable database backups
- [ ] Configure monitoring/logging
- [ ] Set up CI/CD pipeline

---

## Production Best Practices

### Security
1. Use environment variables (never commit secrets)
2. Enable HTTPS/SSL certificates
3. Set secure CORS origins
4. Implement rate limiting
5. Use strong passwords
6. Regular security updates

### Performance
1. Enable caching headers
2. Compress responses (gzip)
3. Use CDN for static files
4. Database query optimization
5. Load balancing for multiple instances

### Monitoring
1. Set up error logging (Sentry, DataDog)
2. Monitor uptime
3. Track API response times
4. Database performance monitoring
5. Alerting for failures

### Database
1. Regular backups
2. Read replicas for scaling
3. Connection pooling
4. Query indexing
5. Maintenance scripts

---

## Troubleshooting

### Frontend not loading
- Check nginx logs: `docker logs tablescout-frontend`
- Verify API proxy configuration
- Check browser console for errors

### Backend connection issues
- Verify database is running: `docker logs tablescout-db`
- Check environment variables
- Verify CORS settings

### Database connection failed
- Ensure PostgreSQL is healthy
- Check credentials in `.env`
- Verify network connectivity

### Build fails
- Clear Docker cache: `docker system prune`
- Rebuild: `docker-compose up --build`
- Check logs for specific errors

---

## Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `DATABASE_URL` | PostgreSQL connection | `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY` | JWT signing key | Generate with: `openssl rand -hex 32` |
| `GEMINI_API_KEY` | Google Gemini API key | Your API key |
| `ENVIRONMENT` | Environment type | `production` or `development` |
| `FRONTEND_URL` | Frontend domain | `https://yourapp.com` |
| `REACT_APP_API_URL` | Backend API URL | `https://api.yourapp.com/api` |

---

## Next Steps

1. Choose deployment platform (Docker Compose, AWS, Render, etc.)
2. Prepare environment variables
3. Build and test locally
4. Deploy to staging first
5. Test thoroughly
6. Deploy to production
7. Set up monitoring and logging

For questions or issues, refer to individual framework documentation:
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [Docker Docs](https://docs.docker.com/)
