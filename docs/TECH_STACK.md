# Technology Stack

## Overview

The Family Office Intelligence system is built using a lightweight Python-based architecture that combines structured data processing, semantic retrieval, large language models, and a Streamlit interface. The technology choices prioritise simplicity, maintainability, and reproducibility while supporting Retrieval-Augmented Generation (RAG).

---

# Core Language & Environment

| Technology | Purpose |
|------------|---------|
| Python 3.10+ | Primary programming language used across the entire project |
| Virtual Environment (.venv) | Dependency isolation and reproducible development environment |
| pip | Python package management |

---

# Data Engineering

| Technology | Purpose |
|------------|---------|
| Pandas | Data loading, cleaning, transformation, validation, and CSV processing |
| NumPy | Numerical operations and data manipulation |
| CSV | Structured storage format for the validated Family Office dataset |

Final dataset:

```
datasets/validated/final_clean_evaluation_v2.csv
```

---

# Embeddings & Semantic Search

## Framework

- Sentence Transformers
- HuggingFace Transformers

## Embedding Model

```
BAAI/bge-small-en-v1.5
```

### Purpose

The embedding model converts both user queries and Family Office records into dense vector representations that enable semantic similarity search.

---

# Vector Store

## FAISS (Facebook AI Similarity Search)

Purpose:

- Store document embeddings
- Fast similarity search
- Efficient nearest-neighbour retrieval
- Local vector indexing
- Low-latency semantic search

---

# Retrieval-Augmented Generation (RAG)

The retrieval pipeline consists of:

- Query embedding
- Semantic retrieval
- Context construction
- Prompt grounding
- Response generation

This architecture ensures that responses are generated using retrieved dataset information instead of relying solely on the language model.

---

# Large Language Model

## Provider

Groq API

## Model

```
llama-3.3-70b-versatile
```

Responsibilities:

- Natural language generation
- Information synthesis
- Query answering
- Response formatting

---

# External APIs

## Tavily API

Purpose:

- Entity discovery
- Public information lookup
- Supplementary web research
- Background enrichment during data collection

---

# Frontend

## Streamlit

Purpose:

- Natural language search interface
- Query submission
- Result presentation
- User interaction

---

## Deployment

Streamlit Cloud

Provides:

- Public web application hosting
- Simple deployment workflow
- Secure secret management

---

# Configuration Management

Environment variables and secrets are used to configure the application.

Examples include:

```
GROQ_API_KEY
TAVILY_API_KEY
DATASET_PATH
EMBEDDING_MODEL
```

Sensitive credentials are excluded from version control.

---

# Version Control

## Git

Used for:

- Source control
- Commit history
- Branch management
- Version tracking

---

## GitHub

Used for:

- Repository hosting
- Collaboration
- Remote backup
- Deployment integration

---

# Development Workflow

Typical workflow:

```
Data Collection
        │
        ▼
Data Cleaning
        │
        ▼
Validation
        │
        ▼
Dataset Generation
        │
        ▼
Embedding Generation
        │
        ▼
FAISS Index
        │
        ▼
Streamlit Application
        │
        ▼
Groq Response Generation
```

---

# Key Design Principles

The technology stack was selected with the following priorities:

- Simple deployment
- Local semantic retrieval
- Lightweight architecture
- Maintainable codebase
- Modular components
- Retrieval-first response generation
- Clear separation between data, retrieval, and presentation layers

---

# Future Technology Enhancements

Potential future improvements include:

- Hybrid keyword + semantic retrieval
- Cross-encoder reranking
- Retrieval evaluation framework
- Automated data refresh pipelines
- Containerisation with Docker
- CI/CD integration
- Authentication and user management
- Monitoring and observability
