import json
import re
from urllib.parse import urlparse
from rapidfuzz import fuzz
from app.discovery.ollama_client import OllamaClient
from app.discovery.prompts import WEBSITE_SELECTION_PROMPT
from app.discovery.search_client import SearchClient

class WebsiteEnricher:
    def __init__(self):
        self.search = SearchClient()
        self.llm = OllamaClient()

    def enrich(self, company):
        name = company.get("name") or company.get("company_name") or ""
        company["name"] = name.strip()
        
        description_text = company.get("description", "") or ""
        website = (company.get("website") or "").strip()
        
        # Safe Extraction from context string if website is missing/bad
        if not self.looks_official(website) or not website:
            extracted_url = self.extract_url_from_text(f"{website} {description_text}")
            if extracted_url and self.looks_official(extracted_url):
                website = extracted_url
                company["website"] = website

        if self.looks_official(website):
            company["website_status"] = "EXISTING"
            return company

        # Credits protection: Only 1 strict targeted Tavily call
        candidates = self.search_candidates(company["name"])
        if not candidates:
            company["website_status"] = "NOT_FOUND"
            return company

        result = self.choose_official(company["name"], candidates)
        company["website"] = result.get("selected_url", "").strip()
        company["website_confidence"] = float(result.get("confidence", 0))
        company["website_reason"] = result.get("reason", "")

        if not company["website"]:
            company["website_status"] = "NOT_FOUND"
            return company

        if not self.looks_official(company["website"]):
            alternative_url = self.extract_url_from_text(company["website_reason"])
            if alternative_url and self.looks_official(alternative_url):
                company["website"] = alternative_url
                company["website_status"] = "FOUND"
                return company
            company["website_status"] = "REVIEW"
            return company

        # Adjusted Threshold to 80 to prevent Alpha vs Alpine Capital confusion
        if not self.domain_matches(company["name"], company["website"]):
            company["website_status"] = "REVIEW"
            return company

        if company["website_confidence"] >= 0.80:
            company["website_status"] = "FOUND"
        else:
            company["website_status"] = "REVIEW"

        return company

    def search_candidates(self, company_name):
        query = f'"{company_name}" official corporate website'
        results = self.search.search(query=query, max_results=4)
        
        # --- SAFE PARSING CHANGES START HERE ---
        raw_list = []
        if isinstance(results, dict):
            raw_list = results.get("results", []) or []
        elif isinstance(results, list):
            raw_list = results
        else:
            raw_list = []
        # --- SAFE PARSING CHANGES END HERE ---

        candidates = []
        seen = set()

        for r in raw_list:
            # Agar individual record dictionary nahi hai toh skip karein (AttributeError se bachne ke liye)
            if not isinstance(r, dict):
                continue
                
            url = r.get("url", "").strip()
            if not url or url in seen:
                continue
            seen.add(url)
            candidates.append({
                "title": r.get("title", ""),
                "url": url,
                "snippet": r.get("content", "")[:300],
            })
        return candidates

    def choose_official(self, company, candidates):
        prompt = f"Company: {company}\nCandidates:\n{json.dumps(candidates, indent=2)}\nSelect official URL."
        try:
            return self.llm.classify(user_prompt=prompt, system_prompt=WEBSITE_SELECTION_PROMPT)
        except Exception:
            valid_ones = [c["url"] for c in candidates if self.looks_official(c["url"])]
            if valid_ones:
                return {"selected_url": valid_ones[0], "confidence": 0.70, "reason": "Fallback"}
            return {"selected_url": "", "confidence": 0.0, "reason": "Failed"}

    def extract_url_from_text(self, text):
        if not text:
            return None
        urls = re.findall(r'(?:Website:\s*|[a-zA-Z0-9.-]+\s*=\s*|https?://)?([a-zA-Z0-9.-]+\.(?:com|net|org|io|co|co\.uk))', text, re.IGNORECASE)
        for url in urls:
            url_clean = url.lower().strip()
            if self.looks_official(url_clean): # Strict directory protection check
                if not url_clean.startswith("http"):
                    return f"https://{url_clean}"
                return url_clean
        return None

    def looks_official(self, url):
        if not url:
            return False
        url = url.lower()
        bad = ["linkedin.com", "pitchbook.com", "crunchbase.com", "rocketreach", "zoominfo.com", "fundcomb", "swfinstitute", "wikipedia", "facebook.com", "twitter.com", "x.com", "youtube.com", "opencorporates", "cbinsights", "altss.com", "fundz.net", "investmentnews.com", "forbes.com", "bloomberg.com"]
        return not any(site in url for site in bad)

    def domain_matches(self, name, url):
        # Fallback helper if domain_matches was called by main pipeline
        try:
            domain = urlparse(url).netloc.replace("www.", "").split(".")[0]
            clean_name = re.sub(r'[^a-zA-Z0-9]', '', name).lower()
            clean_domain = re.sub(r'[^a-zA-Z0-9]', '', domain).lower()
            return fuzz.partial_ratio(clean_name, clean_domain) >= 75
        except Exception:
            return True