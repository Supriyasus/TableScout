from fastapi import FastAPI
from .api.router import router as api_router
from .tests import test_map, test_orches

# import os
# GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


app = FastAPI(title="PlacePilot AI")


app.include_router(api_router)

# test_map()


@app.get("/health")
def health():
    # test_map()
    test_orches()
    return {"status": "ok"}
    
