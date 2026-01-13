from setuptools import setup, find_packages

setup(
    name="rag-service",
    version="0.1.0",
    description="A FastAPI-based Retrieval Augmented Generation service",
    author="Your Name",
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "psycopg2-binary",
        "opensearch-py",
        "pydantic",
        "pydantic-settings",
        "python-dotenv",
        "sqlalchemy",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-asyncio",
            "httpx",
        ],
    },
)
