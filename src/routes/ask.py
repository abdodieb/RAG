from fastapi import APIRouter
from src.schemas.ask import AskRequest, AskResponse, PaperSource

router = APIRouter(prefix="/ask", tags=["Ask"])

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest) -> AskResponse:
    """
    Mock endpoint to handle question asking.
    
    # Week1: Returns hardcoded response for simplicity.
    """

    mock_sources = [
        PaperSource(
            arxiv_id="2101.00001",
            title="A Study on RAG",
            authors=["Author One", "Author Two"],
            abstract_preview="This paper explores..."
        ),
        PaperSource(
            arxiv_id="2102.00002",
            title="Advancements in RAG",
            authors=["Author Three"],
            abstract_preview="In this work, we present..."
        )
    ]
    return AskResponse(
        answer="RAG stands for Retrieval-Augmented Generation...",
        sources=mock_sources
    )