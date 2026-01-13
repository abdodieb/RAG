from typing import Dict, Optional

from pydantic import BaseModel, Field

class ServiceStatus(BaseModel):
    """Individual service status schema."""
    status: str = Field(..., description="service status", example="healthy")
    message: Optional[str] = Field(None, description="Status message", example="Connected successfully")


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str = Field(..., description="Overall system health status", example="healthy")
    version: str = Field(..., description="Application version", example="1.0.0")
    environment: str = Field(..., description="Deployment environment", example="production")
    service_name: str = Field(..., description="Name of the service", example="RAG Service")
    services: Dict[str, ServiceStatus] = Field(..., description="Statuses of individual services")

    class Config:
        """Pydantic configuration for the HealthResponse schema."""
        orm_mode = True
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "environment": "production",
                "service_name": "RAG Service",
                "services": {
                    "database": {
                        "status": "healthy",
                        "message": "Connected successfully"
                    },
                    "cache": {
                        "status": "healthy",
                        "message": "Operational"
                    }
                }
            }
        }

        