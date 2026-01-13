from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from src.deps import SessionDep
from src.repositories.paper import PaperRepository
from src.schemas.paper import PaperResponse

router = APIRouter(prefix="/papers", tags=["Papers"])

@router.get("/{arxiv_id}", response_model=PaperResponse)
async def get_paper_details(
    db: SessionDep, 
    arxiv_id: str = Path(..., description="The arXiv ID of the paper to retrieve")
) -> PaperResponse:
    """Retrieve details of a paper by its arXiv ID.

    Args:
        db (Session): The database session.
        arxiv_id (str): The arXiv ID of the paper.

    Returns:
        PaperResponse: The details of the requested paper.

    Raises:
        HTTPException: If the paper is not found.
    """
    paper_repo = PaperRepository(db)
    paper = paper_repo.get_by_arxiv_id(arxiv_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return PaperResponse.model_validate(paper)