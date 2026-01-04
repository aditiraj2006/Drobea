from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.services.database.mongodb import connect_to_mongo, close_mongo_connection
from app.services.external.firebase_auth import firebase_auth
from app.routes import (
    auth, users, wardrobe, outfits, virtual_tryon, 
    ai_services, social, shopping, analytics, admin
)

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    # Initialize Firebase
    try:
        firebase_auth._initialize_firebase()
    except Exception as e:
        print(f"Warning: Firebase initialization failed: {e}")
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="Drobea API",
    description="AI-Powered Clothing Navigator with Virtual Try-On",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.vercel.app", "*.netlify.app"]
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(wardrobe.router, prefix="/wardrobe", tags=["Wardrobe"])
app.include_router(outfits.router, prefix="/outfits", tags=["Outfits"])
app.include_router(virtual_tryon.router, prefix="/virtual-tryon", tags=["Virtual Try-On"])
app.include_router(ai_services.router, prefix="/ai", tags=["AI Services"])
app.include_router(social.router, prefix="/social", tags=["Social"])
app.include_router(shopping.router, prefix="/shopping", tags=["Shopping"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Drobea API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "drobea-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
