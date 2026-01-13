import logging 
from contextlib import contextmanager
from typing import Generator, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from src.db.interface.base import BaseDatabase

logger = logging.getLogger(__name__)


class PostgresSQLSettings(BaseSettings):
    """PostgreSQL database settings."""

    database_url: str = Field(
        default="postgresql://rag_user:rag_password@localhost:5432/rag_db",
        description="Database connection URL",
    )
    echo_sql: bool = Field(
        default=False,
        description="Enable SQL query logging",
    )
    pool_size: int = Field(
        default=20,
        description="Database connection pool size",
    )
    max_overflow: int = Field(
        default=0,
        description="Maximum overflow size for the connection pool",
    )

    class Config:
        env_prefix = "POSTGRES_"

Base = declarative_base()


class PostgresSQLDatabase(BaseDatabase):
    """PostgreSQL database implementation."""

    def __init__(self, config: PostgresSQLSettings):
        self.config = config
        self.engine: Optional[Engine] = None
        self.SessionLocal: Optional[sessionmaker] = None

    def startup(self) -> None:
        """Initialize the database connection."""
        try:
            logger.info("Starting up PostgreSQL database connection...")
            self.engine = create_engine(
                self.config.database_url,
                echo=self.config.echo_sql,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_pre_ping=True, # Verify connections before use
            ) 
            self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)
            

            assert self.engine is not None  # For type checkers
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                logger.info(f"Database connectivity test result: {result.scalar()}")

            inspector = inspect(self.engine)
            exisitng_tables = inspector.get_table_names()
            logger.info(f"Existing tables in the database: {exisitng_tables}")

            # Create tables if they don't exist (idempotent operation)
            Base.metadata.create_all(bind=self.engine)

            updated_tables = inspector.get_table_names()
            new_tables = set(updated_tables) - set(exisitng_tables)

            if new_tables:
                logger.info(f"New tables created: {new_tables}")
            else:
                logger.info("No new tables were created; all tables already exist.")

            logger.info("PostgreSQL database setup completed successfully.")
            assert self.engine is not None  # For type checkers
            logger.info(f"Database: {self.engine.url}")
            logger.info(f"Total tables: {len(inspector.get_table_names())}")
            logger.info("PostgreSQL database connection established.")

        except Exception as e:
            logger.error(f"Error during PostgreSQL database startup: {e}")
            raise


    def teardown(self) -> None:
        """Close the database connection."""
        if self.engine:
            logger.info("Tearing down PostgreSQL database connection...")
            self.engine.dispose()
            logger.info("PostgreSQL database connection closed.")


    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get a database session context manager."""
        if self.session_factory is None:
            raise RuntimeError("Database session factory is not initialized.")
        session: Session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Session rollback due to error: {e}")
            raise
        finally:
            session.close()