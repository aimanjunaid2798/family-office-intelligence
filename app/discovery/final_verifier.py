import json
from urllib.parse import urlparse
from app.discovery.ollama_client import OllamaClient
from app.discovery.prompts import NORMAL_PROMPT, REVIEW_PROMPT

class FinalVerifier:
    def __init__(self):
        self.llm = OllamaClient()

    def verify(self, company):
        company_name = company.get("name") or company.get("company_name") or ""
        company["company_name"] = company_name
        
        website = company.get("website", "").strip()
        title = company.get("page_title", "") or ""
        meta = company.get("meta_description", "") or ""
        homepage = company.get("homepage_text", "") or ""

        # GPT Fix: If website is completely missing, push to REVIEW instead of instant hard rejection
        if not website:
            company["final_decision"] = "REVIEW"
            company["reason"] = "No website found. Requires manual verification of background notes."
            return company

        text_pool = f"{title} {meta} {homepage}".lower()
        
        # Advanced Name Validation Logic
        name_tokens = [t.lower() for t in company_name.split() if len(t) > 2 and t.lower() not in ["management", "capital", "group", "office", "family", "partners"]]
        name_match_found = any(token in text_pool for token in name_tokens) if name_tokens else company_name.lower() in text_pool

        evidence_score = self.calculate_evidence_score(company, text_pool)
        company["evidence_score"] = evidence_score

        # Strict Multi-page Identity Verification Rule
        family_signatures = ["family office", "single family", "multi family", "private investment office", "generational wealth"]
        has_family_sig = any(sig in text_pool for sig in family_signatures)

        # High confidence match pattern pass
        if name_match_found and has_family_sig and evidence_score >= 4:
            company["final_decision"] = "VERIFIED_FAMILY_OFFICE"
            company["llm_confidence"] = 0.95
            company["reason"] = "Verified via explicit name cross-matching and signature patterns."
            return company

        if not homepage.strip():
            company["final_decision"] = "REVIEW"
            company["reason"] = "Scraped web context payload empty."
            return company

        # Fallback to precise LLM check
        prompt_tmpl = REVIEW_PROMPT if company.get("website_status") == "REVIEW" else NORMAL_PROMPT
        prompt = prompt_tmpl.format(
            company_name=company_name,
            website=website,
            title=title,
            meta=meta,
            homepage=homepage[:6000],
            evidence_score=evidence_score
        )

        result = self.call_llm(prompt)
        company["final_decision"] = result["decision"]
        company["llm_confidence"] = result["confidence"]
        company["reason"] = result["reason"]
        return company

    def calculate_evidence_score(self, company, text_pool):
        score = 4 # Base score
        
        # GPT Fix: Removed hard cut-off. Switched to balanced negative weights framework.
        negative_keywords = ["retail banking", "commercial loans", "insurance agency", "brokerage account", "financial planning firm", "saas platform"]
        positive_keywords = ["family office", "single family office", "multi-family office", "private investment office", "holding company", "principal investments"]

        for kw in negative_keywords:
            if kw in text_pool:
                score -= 3

        for kw in positive_keywords:
            if kw in text_pool:
                score += 2

        if company.get("emails"): score += 1
        if company.get("phones"): score += 1

        return max(0, min(score, 10))

    def call_llm(self, prompt):
        try:
            result = self.llm.classify(user_prompt=prompt, temperature=0)
            decision = str(result.get("decision", "REVIEW")).strip().upper()
            confidence = float(result.get("confidence", 0.50))
            reason = result.get("reason", "Verified via core sequence")

            mapping = {
                "AUTHENTIC": "VERIFIED_FAMILY_OFFICE",
                "VERIFIED": "VERIFIED_FAMILY_OFFICE",
                "VERIFIED_FAMILY_OFFICE": "VERIFIED_FAMILY_OFFICE",
                "REVIEW": "REVIEW",
                "REJECT": "NOT_FAMILY_OFFICE",
                "NOT_FAMILY_OFFICE": "NOT_FAMILY_OFFICE"
            }
            return {"decision": mapping.get(decision, "REVIEW"), "confidence": round(confidence, 2), "reason": reason}
        except Exception as e:
            return {"decision": "REVIEW", "confidence": 0.5, "reason": str(e)}