"""
Health check endpoint.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    """Simple health check for load balancers and monitoring."""
    return {
        "status": "ok",
        "service": "real-estate-lead-bot",
    }
