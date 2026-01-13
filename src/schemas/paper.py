from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

class PaperBase(BaseModel):
    """Base schema for a research paper."""
    arxiv_id: str = Field(..., description="Unique arXiv identifier", example="2101.00001")
    title: str = Field(..., description="Title of the paper", example="A Study on AI")
    authors: List[str] = Field(..., description="List of authors", example=["Alice Smith", "Bob Jones"])
    abstract: str = Field(..., description="Abstract of the paper", example="This paper explores...")
    categories: List[str] = Field(..., description="Categories of the paper", example=["cs.AI", "stat.ML"])
    published_date: datetime = Field(..., description="Publication date", example="2021-01-01T00:00:00Z")
    pdf_url: str = Field(..., description="URL to the PDF of the paper", example="https://arxiv.org/pdf/2101.00001.pdf")


class PaperCreate(PaperBase):
    """Schema for creating a new research paper."""
    pass

class PaperUpdate(BaseModel):
    """Schema for updating an existing research paper."""
    id: UUID = Field(..., description="Unique identifier of the paper", example="123e4567-e89b-12d3-a456-426614174000")
    created_at: datetime = Field(..., description="Creation timestamp", example="2021-01-01T00:00:00Z")
    updated_at: datetime = Field(..., description="Last update timestamp", example="2021-06-01T00:00:00Z")

    class Config:
        from_attributes = True

class PaperResponse(PaperBase):
    """Schema for paper response."""
    id: UUID = Field(..., description="Unique identifier of the paper", example="123e4567-e89b-12d3-a456-426614174000")
    created_at: datetime = Field(..., description="Creation timestamp", example="2021-01-01T00:00:00Z")
    updated_at: datetime = Field(..., description="Last update timestamp", example="2021-06-01T00:00:00Z")

    class Config:
        from_attributes = True


class PaperSearchResponse(BaseModel):
    """Schema for paper search response."""
    papers: List[PaperBase] = Field(..., description="List of papers matching the search criteria")
    total: int = Field(..., description="Total number of papers found", example=100)

