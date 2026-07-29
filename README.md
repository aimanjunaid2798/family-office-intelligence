# Family Office Intelligence & Micro-RAG

## Overview

Family Office Intelligence is an end-to-end AI system designed to discover, validate, structure, and query intelligence on Family Offices through a Retrieval-Augmented Generation (RAG) pipeline.

The primary objective of this project was to build a reliable dataset of validated Family Office records and expose that dataset through a natural language interface. Rather than relying on the language model's internal knowledge, the system retrieves relevant information from a curated dataset before generating a response.

The final dataset contains validated Family Office records stored in:

```
datasets/validated/final_clean_evaluation_v2.csv
```

The application is deployed using Streamlit Cloud and supports natural language querying through a lightweight Micro-RAG architecture.

---

# Key Features

- Family Office discovery and validation pipeline
- Structured dataset generation
- Local semantic search using FAISS
- Retrieval-Augmented Generation (Micro-RAG)
- Natural language search interface
- Grounded responses generated using retrieved evidence
- Streamlit Cloud deployment
- Modular Python-based architecture

---

# System Architecture

```
                User
                  │
                  ▼
          Streamlit Interface
                  │
                  ▼
          Query Processing
                  │
                  ▼
          Embedding Model
                  │
                  ▼
           FAISS Vector Store
                  │
                  ▼
      Relevant Dataset Chunks
                  │
                  ▼
         Groq LLM (Llama 3.3)
                  │
                  ▼
        Grounded Natural Language Response
```

---

# Technology Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.10+ |
| Data Processing | Pandas, NumPy |
| Embeddings | Sentence Transformers |
| Embedding Model | BAAI/bge-small-en-v1.5 |
| Vector Store | FAISS |
| LLM | Groq API |
| Model | llama-3.3-70b-versatile |
| Search | Tavily API |
| Frontend | Streamlit |
| Deployment | Streamlit Cloud |
| Version Control | Git & GitHub |

---

# Dataset

The retrieval system uses the following dataset:

```
datasets/validated/final_clean_evaluation_v2.csv
```

The dataset contains validated Family Office records enriched with structured information used during retrieval.

---

# Retrieval Pipeline

The application follows a Retrieval-Augmented Generation (RAG) workflow.

1. User submits a natural language query.
2. The query is converted into an embedding.
3. FAISS performs semantic similarity search.
4. The most relevant records are retrieved.
5. Retrieved context is supplied to the language model.
6. Groq generates a grounded response based on the retrieved evidence.

---

# Deployment

Frontend

- Streamlit Cloud

Inference

- Groq API

Semantic Search

- FAISS

Embeddings

- BAAI/bge-small-en-v1.5

---

# Example Queries

- Show Family Offices investing in healthcare.
- Find Family Offices located in Singapore.
- Which firms focus on venture capital?
- Show offices with technology investment interests.
- Which Family Offices are based in Europe?

---

# Current Limitations

- The quality of responses depends on the information available within the validated dataset.
- Private Family Offices often disclose limited public information.
- Retrieval quality is influenced by the embedding model and available context.

---

# Future Improvements

- Hybrid semantic and keyword retrieval
- Automated dataset refresh pipeline
- Advanced filtering options
- User authentication
- Retrieval evaluation dashboard
- Continuous data validation workflows

---

# Live Demo

**Streamlit Application**

[https://familyofficeintelligence.streamlit.app/](https://familyofficeintelligence.streamlit.app/)

---

# GitHub Repository

[https://github.com/aimanjunaid2798/family-office-intelligence/](https://github.com/aimanjunaid2798/family-office-intelligence/)

---

# License

This repository was developed as part of the PolarityIQ Differentiator Assessment.

All work, code, datasets, and documentation remain the intellectual property of the author.
