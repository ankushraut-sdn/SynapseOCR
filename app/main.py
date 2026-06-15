import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import router

app = FastAPI(title="smartVision OCR API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")

# Mount the static directory to serve static assets directly if needed
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include the endpoints router
app.include_router(router)
