# RAG (Retrieval-Augmented Generation) System Design

## Project Overview
This is a RAG system designed to enhance LLM responses by retrieving relevant context from a knowledge base before generation. The architecture follows a modern microservices approach with FastAPI backend, vector database integration, and workflow orchestration.

---

## Project Structure

```
RAG/
├── compose.yml              # Docker Compose configuration for orchestrating all services
│                            # (API server, vector DB, Airflow, Redis/cache)
│
├── design.md               # This file - architectural design and documentation
│
├── airflow/                # Apache Airflow DAGs and workflow orchestration
│   │                       # Purpose: Schedule and manage ETL pipelines for document ingestion
│   │                       # - Data ingestion workflows
│   │                       # - Periodic re-indexing tasks
│   │                       # - Document processing pipelines
│   └── (DAG files)
│
├── src/                    # Main application source code
│   │
│   ├── config.py          # Application configuration and settings
│   │                      # - Environment variables loading
│   │                      # - Database connection strings
│   │                      # - Vector DB settings (Pinecone/Qdrant/Weaviate)
│   │                      # - LLM API keys and endpoints
│   │                      # - Embedding model configurations
│   │
│   ├── deps.py            # Dependency injection container
│   │                      # - Database session management
│   │                      # - Service layer dependencies
│   │                      # - Authentication/authorization dependencies
│   │                      # - Vector store client initialization
│   │
│   ├── main.py            # FastAPI application entry point
│   │                      # - App initialization
│   │                      # - Route registration
│   │                      # - Middleware setup (CORS, logging, auth)
│   │                      # - Startup/shutdown events
│   │
│   ├── db/                # Database layer
│   │   │                  # Purpose: Handle persistent storage operations
│   │   ├── base.py       # SQLAlchemy Base class and session management
│   │   ├── session.py    # Database session factory and connection pooling
│   │   └── migrations/   # Alembic migrations for schema versioning
│   │
│   ├── models/            # Database ORM models (SQLAlchemy)
│   │   │                  # Purpose: Define database schema and relationships
│   │   ├── document.py   # Document metadata (title, source, timestamps)
│   │   ├── chunk.py      # Text chunks with embeddings references
│   │   ├── user.py       # User authentication and profiles
│   │   └── query.py      # Query history and analytics
│   │
│   ├── repositories/      # Data access layer (Repository pattern)
│   │   │                  # Purpose: Abstract database operations from business logic
│   │   ├── document_repo.py    # CRUD operations for documents
│   │   ├── chunk_repo.py       # Chunk storage and retrieval
│   │   ├── vector_repo.py      # Vector database operations
│   │   └── user_repo.py        # User management queries
│   │
│   ├── routes/            # API endpoints (FastAPI routers)
│   │   │                  # Purpose: HTTP request handlers and routing
│   │   ├── chat.py       # RAG query endpoint (main user interaction)
│   │   ├── documents.py  # Document upload and management
│   │   ├── search.py     # Semantic search endpoints
│   │   └── auth.py       # Authentication routes (login/register)
│   │
│   ├── schemas/           # Pydantic models for request/response validation
│   │   │                  # Purpose: Data validation and API contracts
│   │   ├── chat.py       # ChatRequest, ChatResponse schemas
│   │   ├── document.py   # DocumentCreate, DocumentResponse schemas
│   │   ├── search.py     # SearchQuery, SearchResult schemas
│   │   └── user.py       # UserCreate, UserLogin, UserResponse schemas
│   │
│   └── services/          # Business logic layer
│       │                  # Purpose: Core application functionality
│       ├── embedding_service.py    # Generate embeddings (OpenAI/Sentence-Transformers)
│       ├── vector_service.py       # Vector store operations (index, search)
│       ├── llm_service.py          # LLM integration (OpenAI/Anthropic/local models)
│       ├── rag_service.py          # RAG pipeline orchestration
│       ├── document_processor.py   # Parse and chunk documents (PDF, TXT, DOCX)
│       └── auth_service.py         # JWT token generation and validation
│
├── static/                # Static assets
│   │                      # Purpose: Serve frontend files and media
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript/TypeScript frontend code
│   └── uploads/          # Temporary upload storage
│
└── tests/                # Test suite
    │                      # Purpose: Ensure code quality and correctness
    ├── unit/             # Unit tests for services and utilities
    ├── integration/      # Integration tests for API endpoints
    └── fixtures/         # Test data and mock objects
```

---

## Architecture Overview

### 1. **API Layer** (FastAPI)
- RESTful endpoints for RAG queries, document management, and search
- WebSocket support for streaming responses
- Authentication and rate limiting

### 2. **Service Layer**
- **RAG Pipeline**: Retrieve relevant chunks → Inject into prompt → Generate response
- **Embedding Service**: Convert text to vector representations
- **Vector Service**: Store and search embeddings (Pinecone/Qdrant/Weaviate)
- **LLM Service**: Interface with language models (OpenAI, Anthropic, local)

### 3. **Data Layer**
- **PostgreSQL**: Metadata storage (documents, users, query logs)
- **Vector Database**: High-dimensional similarity search
- **Repository Pattern**: Clean separation of data access logic

### 4. **Workflow Orchestration** (Airflow)
- Scheduled document ingestion from various sources
- Batch processing and re-indexing
- Data quality checks and monitoring

### 5. **Containerization** (Docker Compose)
- Isolated service deployment
- Easy local development and production deployment
- Service discovery and networking

---

## Data Flow

### RAG Query Flow:
1. **User Query** → API Endpoint ([routes/chat.py](routes/chat.py))
2. **Generate Embedding** → Embedding Service
3. **Vector Search** → Vector Database (retrieve top-k chunks)
4. **Context Injection** → Build prompt with retrieved context
5. **LLM Generation** → Generate response using augmented prompt
6. **Response** → Return to user with citations

### Document Ingestion Flow:
1. **Upload Document** → [routes/documents.py](routes/documents.py)
2. **Parse & Chunk** → Document Processor Service
3. **Generate Embeddings** → Embedding Service
4. **Store Vectors** → Vector Database
5. **Save Metadata** → PostgreSQL
6. **Index Complete** → Ready for retrieval

---

## Technology Stack

- **Framework**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL + SQLAlchemy ORM
- **Vector Store**: Pinecone/Qdrant/Weaviate (configurable)
- **Embeddings**: OpenAI API / Sentence-Transformers
- **LLM**: OpenAI GPT-4 / Anthropic Claude / Local models
- **Orchestration**: Apache Airflow
- **Containerization**: Docker + Docker Compose
- **Testing**: Pytest

---

## Key Design Patterns

1. **Repository Pattern**: Separation of data access logic
2. **Dependency Injection**: Managed via [deps.py](deps.py)
3. **Service Layer Pattern**: Business logic isolation
4. **Schema Validation**: Pydantic models for type safety
5. **Configuration Management**: Environment-based settings

---

## Future Enhancements

- [ ] Multi-modal RAG (images, tables, charts)
- [ ] Advanced chunking strategies (semantic chunking)
- [ ] Query expansion and rewriting
- [ ] Response caching with Redis
- [ ] A/B testing framework for RAG parameters
- [ ] Observability and monitoring (Prometheus/Grafana)
- [ ] Fine-tuned embedding models
- [ ] Hybrid search (keyword + semantic)

---

## Getting Started

```bash
# Start all services
docker-compose up -d

# Run database migrations
alembic upgrade head

# Access API documentation
http://localhost:8000/docs

# Access Airflow UI
http://localhost:8080
```

---

**Last Updated**: January 5, 2027
