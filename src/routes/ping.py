from fastapi import APIRouter
from sqlalchemy import text

from src.deps import DatabaseDep, SettingsDep
from src.schemas.health import HealthResponse, ServiceStatus



router = APIRouter()

@router.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check(
    settings: SettingsDep = SettingsDep,
    database: DatabaseDep = DatabaseDep,
) -> HealthResponse:
    """Health check endpoint to verify system status.

    Returns:
        HealthResponse: The health status of the system.
    """
    # Check database connectivity
    try:
        with database.get_session() as session:
            session.execute(text("SELECT 1"))
        db_status = ServiceStatus(status="healthy", message="Connected successfully")
    except Exception as e:
        db_status = ServiceStatus(status="unhealthy", message=str(e))

    overall_status = "healthy" if db_status.status == "healthy" else "unhealthy"

    return HealthResponse(
        status=overall_status,
        version=settings.app_version,
        environment=settings.environment,
        service_name="RAG Service",
        services={
            "database": db_status
        }
    )