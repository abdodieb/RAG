from contextlib import contextmanager
from src.db.factory import make_database


# Global variable to hold the database instance
_database = None

def get_database():
    """
    Get the global database instance, creating it if it doesn't exist.

    Returns:
        BaseDatabase: The global database instance.
    """
    global _database
    if _database is None:
        _database = make_database()
    return _database

@contextmanager
def get_db_session():
    """
    Context manager to provide a database session.

    Yields:
        Session: A database session.
    """
    database = get_database()
    with database.get_session() as session:
        yield session

