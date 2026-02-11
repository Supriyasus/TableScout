from fastapi import FastAPI, Depends
from backend.api.router import router as api_router
from backend.api.v1.auth import router as auth_router
from backend.db.session import get_db
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="TableScout Backend")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origins=[ 
        "https://table-scout.netlify.app", # Replace with your actual Netlify URL 
        "http://localhost:3000" # Optional: for local development 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(api_router)

@app.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        # Simple DB check: run a lightweight query
        db.execute("SELECT 1")
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "db": "not connected", "detail": str(e)}
