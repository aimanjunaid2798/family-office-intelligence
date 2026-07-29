# Limitations & Future Work

# Overview

The current implementation satisfies the objectives of the assessment by providing a validated Family Office dataset, a working Micro-RAG pipeline, and a deployed customer-facing application. However, several practical limitations remain and represent opportunities for future improvement.

---

# Current Limitations

## 1. Public Data Availability

Many Single Family Offices intentionally maintain a limited public presence.

As a result, certain fields such as direct contact information, investment mandates, or recent investment activity cannot always be independently verified through publicly available sources.

Rather than estimating missing values, the dataset preserves uncertainty where appropriate.

---

## 2. Dataset Coverage

The retrieval system is limited to the information contained within the indexed dataset.

The application does not perform real-time web retrieval during user queries, meaning newly published information is not automatically reflected until the dataset is refreshed and re-indexed.

---

## 3. Semantic Retrieval Limitations

The current implementation relies on dense vector similarity through FAISS.

Although semantic retrieval performs well for natural language queries, similar organisations with overlapping descriptions may occasionally produce less relevant retrieval results.

---

## 4. Lightweight User Interface

The Streamlit application focuses on demonstrating the complete retrieval workflow rather than providing a feature-rich analytics platform.

Advanced filtering, dashboards, authentication, and collaborative features are intentionally outside the scope of the current implementation.

---

## 5. Evaluation Scope

Testing primarily focused on functional correctness and retrieval quality.

A larger-scale evaluation involving diverse user queries and retrieval benchmarking would provide additional insight into overall system performance.

---

# Future Improvements

Given additional development time, the following enhancements would be prioritised.

## Data Pipeline

- Automated dataset refresh pipeline
- Scheduled validation workflow
- Incremental indexing
- Additional validation checks
- Expanded Family Office coverage

---

## Retrieval

- Hybrid keyword and semantic retrieval
- Metadata filtering
- Cross-encoder reranking
- Retrieval quality evaluation
- Confidence scoring for retrieved documents
- Source citation generation

---

## User Experience

- Advanced search filters
- Saved searches
- Interactive dashboards
- Export functionality
- User authentication
- Search history

---

## Engineering

- Docker containerisation
- Automated testing
- CI/CD pipeline
- Monitoring and logging
- Configuration management improvements
- Performance optimisation

---

# Closing Remarks

The current implementation demonstrates a complete end-to-end workflow for validated Family Office retrieval and question answering.

Future work would focus on expanding dataset coverage, improving retrieval quality, and enhancing the overall user experience while maintaining the same emphasis on reliable, evidence-based responses.
