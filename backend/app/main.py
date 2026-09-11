"""FastAPI application entry point."""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import health, chat, internal

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Real Estate Lead Bot API",
    description="PrimeHomes Realty — Lead management API for n8n workflows",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(internal.router, prefix="/api/v1", tags=["internal"])


@app.get("/")
def root():
    return {
        "service": "Real Estate Lead Bot API",
        "version": "0.2.0",
        "docs": "/docs",
        "health": "/api/v1/health",
    }
