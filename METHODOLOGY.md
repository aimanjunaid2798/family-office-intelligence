# Methodology

# Overview

The objective of this project was to build a validated Family Office dataset and expose it through a Retrieval-Augmented Generation (RAG) system. The methodology prioritised data quality, validation, and retrieval reliability over dataset size or interface complexity.

The overall workflow consisted of five stages:

1. Discovery
2. Enrichment
3. Validation
4. Dataset Generation
5. Retrieval and Question Answering

---

# 1. Discovery

Potential Family Offices were identified using multiple public sources rather than relying on a single directory. The goal was to minimise source bias and improve coverage.

Examples of information gathered during discovery included:

- Organisation name
- Headquarters
- Public website
- Business description
- Initial Family Office classification

Records that could not be reasonably associated with a Family Office were excluded from further processing.

---

# 2. Enrichment

After discovery, each candidate record was enriched using publicly available information.

Where available, additional information included:

- Investment focus
- Geographic presence
- Industry interests
- Contact information
- Recent business activity
- Public company profile

Not every record contained every field. Missing information was retained as missing rather than inferred.

---

# 3. Validation

Validation was performed at two levels.

## Record Validation

Each organisation was reviewed to determine whether sufficient evidence existed to classify it as a Family Office.

Records with insufficient evidence or conflicting information were excluded from the final dataset.

## Field Validation

Individual fields were reviewed independently.

Where information could not be confirmed from available public sources, the value was left blank instead of being estimated.

This approach prioritised data reliability over completeness.

---

# 4. Dataset Generation

Validated records were consolidated into the final structured dataset.

Dataset Location

```
datasets/validated/final_clean_evaluation_v2.csv
```

The dataset serves as the single source of truth for retrieval.

No information is generated directly from the language model without first retrieving supporting context from this dataset.

---

# 5. Retrieval Pipeline

The completed dataset is indexed using semantic embeddings.

The retrieval workflow is:

User Query

↓

Embedding Generation

↓

FAISS Similarity Search

↓

Relevant Dataset Records

↓

Prompt Construction

↓

Groq LLM

↓

Grounded Response

Only the retrieved context is supplied to the language model during answer generation.

---

# Source Categories

Different source categories served different purposes during the pipeline.

| Source Category | Purpose |
|-----------------|---------|
| Discovery Sources | Identify potential Family Offices |
| Organisation Websites | Verify organisation details |
| Public Business Profiles | Confirm organisational information |
| Professional Profiles | Validate people and organisational relationships |
| News and Public Announcements | Capture recent activity and investment signals |

---

# Validation Philosophy

The project prioritised trustworthy information over complete information.

When supporting evidence was unavailable, values were intentionally left blank instead of being inferred.

This reduces the risk of presenting unsupported information as factual.

---

# Known Limitations

Several limitations remain.

- Some Family Offices maintain very limited public visibility.
- Public information may change over time.
- Certain contact details cannot always be independently verified.
- Retrieval quality depends on the information available within the validated dataset.

These limitations are reflected in the final dataset rather than being hidden through estimation or language-model generated content.
