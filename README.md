# Family Office Intelligence & Micro-RAG Pipeline

A production-grade, end-to-end AI system that discovers, validates, structures, and queries verified Single-Family Office (SFO) intelligence. Developed as part of the PolarityIQ / Falcon Scaling Technical Assessment (Stage 1).

---

## 🚀 Live Demonstration
- **Live Streamlit App:** [Access Live App URL Here] *(Replace with your Streamlit Cloud URL)*
- **GitHub Repository:** [https://github.com/aimanjunaid2798/family-office-intelligence](https://github.com/aimanjunaid2798/family-office-intelligence)

---

## 📊 Overview & Architecture
Single-Family Offices manage private wealth for ultra-high-net-worth individuals and notoriously lack public digital footprints. This system bridges the intelligence gap by combining automated discovery, rigorous multi-tier data validation, semantic chunking, and a Retrieval-Augmented Generation (RAG) engine designed for high-intent fund managers and investors.

### Core Pipeline Components:
1. **Discovery & Sourcing Engine:** Targeted ingestion pipeline designed to isolate true Single-Family Offices (SFOs) from generic multi-family offices (MFOs) and wealth advisory firms.
2. **Enrichment & Verification Layer:** Extracts high-value cells including asset allocation mandates, AUM, decision-maker (principal) details, direct professional contacts, and dated recent activities. Every cell carries explicit verification lineage.
3. **Micro-RAG & Retrieval Core:** Powered by local vector embeddings and advanced semantic search to query unstructured and structured FO profiles with strict hallucination controls.
4. **Interactive Presentation Layer:** Built with Streamlit, offering clean query interfaces, entity inspection, and real-time confidence metrics.

---

## 🛠️ Tech Stack & Architecture Choices

| Component | Technology Selected | Rationale |
| :--- | :--- | :--- |
| **Language & Environment** | Python 3.10+ | Industry standard for ML/AI engineering workflows. |
| **Data Processing** | Pandas / NumPy | High-performance tabular cleaning and validation checks. |
| **Embeddings & Vectorization** | `BAAI/bge-small-en-v1.5` | Exceptional retrieval accuracy for semantic search relative to model size. |
| **LLM & Inference** | Groq API (`llama-3.3-70b-versatile`) | Ultra-low latency inference with strong reasoning capabilities for financial data. |
| **Vector Store / Retrieval** | ChromaDB / FAISS (Local Vector Index) | Lightweight, reliable vector storage optimized for Micro-RAG deployment. |
| **Web UI Framework** | Streamlit Cloud | Clean, responsive, and robust deployment interface for client-facing demos. |

---

## 📁 Dataset & Schema Structure
The final dataset (`final_clean_evaluation_v2.csv`) contains **55 rigorously validated production records** adhering strictly to the dual-rule proof standard:
- **Rule 1 (Cells):** Every data point carries provenance and verification basis; unverified fields are explicitly marked as honest blanks.
- **Rule 2 (Firms):** Affirmative evidence required to confirm single-family office classification prior to dataset inclusion.

### Key Fields Included:
- Entity Identity & Classification (SFO vs MFO)
- Investment Theses, Focus Sectors, and Asset Class Mandates
- Principal / Decision-Maker Information (Name, Title, Verified LinkedIn, Direct Work Contact)
- Recent Activity & Dated Signals (Co-investments, key hires, capital commitments)
- Verification Basis & Confidence Scoring

---

## 🚀 Local Installation & Running Guide

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/aimanjunaid2798/family-office-intelligence.git](https://github.com/aimanjunaid2798/family-office-intelligence.git)
   cd family-office-intelligence
