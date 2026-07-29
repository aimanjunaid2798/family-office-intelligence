# Engineering Decisions

## Design Philosophy

The primary objective of this project was not to maximise the number of features, but to build a system that produces reliable, explainable, and grounded responses from a validated Family Office dataset.

Throughout development, engineering decisions were guided by a simple principle:

> The quality of the retrieval system can never exceed the quality of the underlying data.

For this reason, a significant portion of development effort was invested in data processing, validation, and retrieval rather than interface complexity.

---

# Major Engineering Decisions

## 1. Data-First Development

Instead of beginning with the user interface, development started with the data pipeline.

The reasoning was straightforward: a polished interface provides little value if the underlying records are inaccurate, duplicated, or weakly supported.

Priority was therefore given to:

- record discovery
- validation
- data cleaning
- enrichment
- retrieval readiness

Only after these components were functioning was the user interface developed.

---

## 2. Retrieval-Augmented Generation Instead of Direct LLM Responses

The language model was not used as the primary knowledge source.

Instead, every response follows a retrieval-first workflow.

User Query

↓

Semantic Retrieval

↓

Relevant Dataset Records

↓

LLM Response

This approach helps keep responses grounded in the indexed dataset rather than relying solely on the model's internal knowledge.

---

## 3. Local Semantic Search Using FAISS

FAISS was selected as the vector index because it provides efficient local similarity search with minimal operational overhead.

For a project of this scale, it offered an appropriate balance between performance, simplicity, and ease of deployment.

---

## 4. Lightweight Frontend

The Streamlit interface was intentionally kept simple.

Rather than investing significant time in dashboards, animations, or advanced visualisations, development effort remained focused on the core workflow:

- accepting natural language queries
- retrieving relevant records
- presenting readable responses

This prioritisation reflects the project's emphasis on functionality and reliability.

---

## 5. Separation of Responsibilities

The system was designed around clearly separated components.

- Data preparation
- Embedding generation
- Vector indexing
- Retrieval
- Response generation
- User interface

Keeping these responsibilities separate makes the project easier to understand, test, and extend.

---

# Trade-offs

Every engineering decision involves compromise.

Several conscious trade-offs were made during development.

| Prioritised | Deferred |
|-------------|----------|
| Data validation | Advanced dashboard features |
| Retrieval quality | UI customisation |
| Simpler architecture | Additional framework complexity |
| Reliable responses | Large feature set |
| Maintainability | Premature optimisation |

These decisions were made intentionally to maximise the quality of the assessment deliverables within the available development time.

---

# Lessons Learned

Building the project reinforced several practical observations.

Reliable retrieval begins with reliable data.

Validation is often more time-consuming than model integration.

Small architectural decisions made early in development have a significant impact on maintainability later.

Keeping components modular simplifies testing and future improvements.

---

# Future Engineering Improvements

If additional development time were available, the next priorities would include:

- automated testing
- CI/CD pipeline
- Docker-based deployment
- retrieval evaluation metrics
- hybrid keyword and semantic retrieval
- metadata filtering
- cross-encoder reranking
- user authentication
- monitoring and logging
- incremental dataset updates

These improvements would strengthen the operational maturity of the application while preserving the existing retrieval pipeline.

---

# Conclusion

The project was developed with an emphasis on dependable retrieval, modular architecture, and evidence-based responses.

Where trade-offs were required, preference was consistently given to improving the quality of the underlying data and retrieval pipeline rather than expanding the user interface or feature count.
