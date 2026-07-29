# Retrieval-Augmented Generation (RAG) Documentation

# Overview

The application uses a lightweight Retrieval-Augmented Generation (Micro-RAG) architecture to answer natural language queries against a validated Family Office dataset.

Instead of relying solely on the language model's internal knowledge, the system retrieves relevant information from the dataset before generating a response. This retrieval-first approach helps keep responses grounded in the available evidence.

---

# Dataset

The retrieval pipeline operates on the validated dataset located at:

```
datasets/validated/final_clean_evaluation_v2.csv
```

This dataset serves as the primary knowledge source for the application.

---

# Micro-RAG Architecture

```
User Query
      │
      ▼
Generate Query Embedding
      │
      ▼
Semantic Search (FAISS)
      │
      ▼
Top Matching Records
      │
      ▼
Prompt Construction
      │
      ▼
Groq LLM
      │
      ▼
Grounded Response
```

---

# Embedding Model

**Framework**

- Sentence Transformers
- HuggingFace Transformers

**Embedding Model**

```
BAAI/bge-small-en-v1.5
```

### Why this model?

The model was selected because it provides:

- Strong semantic retrieval performance
- Small inference footprint
- Fast embedding generation
- Good balance between accuracy and computational cost

These characteristics make it suitable for a lightweight Micro-RAG application.

---

# Vector Store

The application uses **FAISS (Facebook AI Similarity Search)** as the local vector database.

Responsibilities include:

- storing document embeddings
- semantic similarity search
- efficient nearest-neighbour retrieval
- low-latency local querying

---

# Document Chunking Strategy

Each Family Office record is converted into a structured text document before embedding.

A typical document contains information such as:

- organisation name
- location
- investment focus
- business description
- contact information (when available)
- additional structured attributes

Each document is embedded independently.

This record-level chunking preserves context while keeping retrieval straightforward and interpretable.

---

# Retrieval Strategy

For every user query the system performs the following steps:

1. Generate an embedding for the user query.
2. Search the FAISS index for the most similar records.
3. Retrieve the highest-ranked matches.
4. Build a context window from the retrieved documents.
5. Send only the retrieved context to the language model.
6. Generate a natural language response.

---

# Prompt Grounding

The language model is instructed to answer using the retrieved context.

If the retrieved evidence is insufficient, the response should acknowledge that the available dataset does not contain enough information instead of introducing unsupported claims.

This design reduces the likelihood of responses extending beyond the available evidence.

---

# Language Model

Inference is performed using the Groq API.

Model:

```
llama-3.3-70b-versatile
```

The language model is responsible for:

- synthesising retrieved information
- answering user questions
- presenting information in natural language

The model is not intended to replace the dataset as the source of truth.

---

# Example Queries

The deployed application was tested using queries such as:

- Show Family Offices investing in healthcare.
- Find Family Offices located in Singapore.
- Which Family Offices invest in technology?
- Show Family Offices based in Europe.
- Find Family Offices interested in venture capital.
- Which offices have investment activity related to fintech?

These queries were used to verify retrieval quality and response generation.

---

# Retrieval Controls

The application includes several controls intended to improve response quality.

- Retrieval is performed before generation.
- Responses are based on retrieved dataset records.
- The dataset acts as the primary knowledge source.
- Missing information is not replaced with generated values.
- When evidence is limited, the response reflects that limitation.

---

# Current Limitations

Current limitations include:

- Retrieval quality depends on the embedding model.
- Public information about Family Offices is often incomplete.
- Similar organisations may retrieve overlapping results.
- The system is limited to the information contained within the indexed dataset.

---

# Production Dataset

The validation pipeline processes candidate records through multiple validation stages. During this process, records may be marked as **Accepted**, **Review**, or **Rejected** for audit and quality assurance purposes.

Although the validation workflow tracks Accepted, Review, and Rejected outcomes for auditing purposes, only the validated Family Office records are indexed into the FAISS vector database. The deployed RAG application retrieves information exclusively from this validated production index. Only records that satisfy the project's inclusion criteria are indexed into the FAISS vector database and exposed through the deployed RAG application.

Records marked for manual review or rejection are retained as part of the validation workflow but are not included in the customer-facing retrieval index.

---

# Future Improvements

Potential future enhancements include:

- Hybrid keyword and semantic retrieval
- Metadata filtering
- Cross-encoder reranking
- Retrieval quality evaluation
- Incremental index updates
- Multi-vector retrieval
- Citation-aware responses
- User feedback driven retrieval optimisation
