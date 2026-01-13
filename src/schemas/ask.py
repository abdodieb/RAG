from typing import List

from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    """Schema for ask request."""
    question: str = Field(..., description="The question to be answered", example="What is RAG?")

class PaperSource(BaseModel):
    """Schema for paper source information."""
    arxiv_id: str = Field(..., description="The arXiv ID of the paper", example="2101.00001")
    title: str = Field(..., description="The title of the paper", example="A Study on RAG")
    authors: List[str] = Field(..., description="List of authors", example=["Author One", "Author Two"])
    abstract_preview: str = Field(..., description="Abstract of the paper", example="This paper explores...")

class AskResponse(BaseModel):
    """Schema for ask response."""
    answer: str = Field(..., description="The answer to the question", example="RAG stands for Retrieval-Augmented Generation...")
    sources: List[PaperSource] = Field(..., description="List of paper sources used to generate the answer")

    class Config:
        """Pydantic configuration for the AskResponse schema."""
        orm_mode = True