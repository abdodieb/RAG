from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models.paper import Paper
from src.schemas.paper import PaperCreate

class PaperRepository:
    """Repository for managing research papers in the database."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, paper: PaperCreate) -> Paper:
        """Create a new research paper record in the database.

        Args:
            paper (PaperCreate): The paper data to create.

        Returns:
            Paper: The created paper record.
        """
        db_paper = Paper(**paper.model_dump())
        self.session.add(db_paper)
        self.session.commit()
        self.session.refresh(db_paper)
        return db_paper
    
    def get_by_arxiv_id(self, arxiv_id: str) -> Optional[Paper]:
        """Retrieve a research paper by its arXiv ID.

        Args:
            arxiv_id (str): The arXiv ID of the paper.

        Returns:
            Optional[Paper]: The paper record if found, else None.
        """
        return self.session.query(Paper).filter(Paper.arxiv_id == arxiv_id).first()
    
    def get_by_id(self, paper_id: UUID) -> Optional[Paper]:
        """Retrieve a research paper by its unique ID.

        Args:
            paper_id (UUID): The unique ID of the paper.

        Returns:
            Optional[Paper]: The paper record if found, else None.
        """
        return self.session.query(Paper).filter(Paper.id == paper_id).first()
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[Paper]:
        """Retrieve all research papers with pagination.

        Args:
            limit (int): The maximum number of records to return.
            offset (int): The number of records to skip.

        Returns:
            List[Paper]: A list of paper records.
        """
        return self.session.query(Paper).order_by(Paper.published_date.desc()).limit(limit).offset(offset).all()
    
    def update(self, paper: Paper) -> Paper:
        """Update an existing research paper record in the database.

        Args:
            paper (Paper): The paper record to update.

        Returns:
            Paper: The updated paper record.
        """
        self.session.add(paper)
        self.session.commit()
        self.session.refresh(paper)
        return paper
    
    def upsert(self, paper_create: PaperCreate) -> Paper:
        """Insert or update a research paper record based on arXiv ID.

        Args:
            paper_data (PaperCreate): The paper data to insert or update.
        Returns:
            Paper: The inserted or updated paper record.
        """
        existing_paper = self.get_by_arxiv_id(paper_create.arxiv_id)
        if existing_paper:
            # Update existing paper
            for key, value in paper_create.model_dump(exclude_unset=True):
                setattr(existing_paper, key, value)
            return self.update(existing_paper)
        else:
            # Create new paper
            return self.create(paper_create)
        
        
        