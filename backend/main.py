from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.router import router as api_router

app = FastAPI(title="PlacePilot AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # in production, replace with domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
def health():
    return {"status": "ok"}
