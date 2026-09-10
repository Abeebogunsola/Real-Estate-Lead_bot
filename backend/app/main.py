"""
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import health

app = FastAPI(
    title="Real Estate Lead Bot API",
    description="API for PrimeHomes Realty Lead Management System",
    version="0.1.0",
)

# CORS — will be driven by settings later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])


@app.get("/")
def root():
    return {
        "service": "Real Estate Lead Bot API",
        "version": "0.1.0",
        "docs": "/docs",
    }
