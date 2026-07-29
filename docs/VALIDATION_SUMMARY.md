# Validation Summary

# Overview

Validation was performed as a separate stage after discovery and enrichment.

The objective was not simply to collect potential Family Offices, but to determine whether each candidate record met the project's inclusion criteria before being retained in the final workflow.

Each candidate passed through a structured validation process that evaluated:

- Organisation identity
- Family Office classification
- Website authenticity
- Supporting evidence
- Publicly verifiable information
- Overall confidence

Records that did not satisfy the required validation standard were either marked for manual review or rejected.

---

# Validation Workflow

```
Discovery

↓

Enrichment

↓

Website Validation

↓

Evidence Review

↓

Classification

↓

Final Decision
```

---

# Validation Criteria

Each record was evaluated using multiple signals including:

- organisation identity
- public website
- supporting business description
- available contact information
- evidence collected during enrichment
- verification notes
- confidence score

The final decision was recorded as one of:

- Accepted
- Review
- Rejected

---

# Example Validation Records

## Example 1 — Bayshore Global Management

### Discovery

- Discovery Source: Tavily

### Initial Finding

The organisation was identified during the discovery stage as a potential Family Office.

### Validation Findings

- No official website could be confidently resolved.
- Limited publicly verifiable information was available.
- Website validation was unsuccessful.

### Evidence

- Website Status: **NOT_FOUND**
- Verification Status: **Verified**
- Final Decision: **REVIEW**

### Reason

The available evidence was insufficient to confidently include the organisation without additional manual investigation.

---

## Example 2 — Brown Brothers Harriman Capital Partners

### Discovery

- Discovery Source: Tavily

### Validation Findings

During validation, the retrieved website described a broader investment and financial services organisation rather than a clearly identifiable Family Office.

### Evidence

- Existing website identified
- Validation determined the entity did not satisfy the required Family Office criteria.
- Website validation indicated a mismatch with the intended entity type.

### Final Decision

**Rejected**

### Reason

Although the organisation maintains a legitimate public presence, the available evidence did not support inclusion under the project's Family Office classification criteria.

---

## Example 3 — Generic Candidate Record

Several candidate organisations entered the pipeline with incomplete or conflicting public information.

Typical validation outcomes included:

- insufficient supporting evidence
- missing official website
- conflicting business descriptions
- inability to verify organisational classification

Rather than attempting to infer missing information, these records were either flagged for manual review or excluded from the production dataset.

---

# Validation Philosophy

A core design principle of the project was to favour evidence over completeness.

When sufficient public evidence could not be established, the record was not promoted as a validated Family Office.

Similarly, individual fields that could not be confirmed were left blank rather than populated with estimated values.

This approach prioritises transparency and reduces the likelihood of presenting unsupported information as factual.

---

# Validation Limitations

Some Family Offices intentionally maintain a minimal public presence.

Consequently:

- websites may not exist
- contact information may not be publicly available
- investment activity may be difficult to verify
- organisation type may remain uncertain

These limitations are reflected in the validation outcome instead of being hidden through assumptions.

---

# Conclusion

The validation stage acts as the quality control layer of the pipeline.

Rather than treating discovery as sufficient evidence, each candidate record is independently reviewed before inclusion.

This process improves the overall reliability of the retrieval dataset and ensures that the deployed RAG system operates on information that has undergone structured validation.
