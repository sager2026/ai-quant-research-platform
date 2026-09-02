from fastapi import APIRouter


router = APIRouter()


@router.get(
    "/health",
    tags=["System"],
)
def health() -> dict[str, str]:
    """
    Basic service health endpoint.

    This verifies that Uvicorn and FastAPI are running
    and able to serve HTTP requests.
    """

    return {
        "status": "ok",
        "service": "QuantMind",
    }