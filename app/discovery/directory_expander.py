import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from app.discovery.search_client import SearchClient


class DirectoryExpander:

    COMPANY_KEYWORDS = {
        "capital",
        "partners",
        "investment",
        "investments",
        "holding",
        "holdings",
        "ventures",
        "trust",
        "group",
        "management",
        "asset",
        "wealth",
        "advisors",
        "advisers",
    }

    NEGATIVE_WORDS = {
        "privacy",
        "terms",
        "cookies",
        "contact",
        "login",
        "register",
        "subscribe",
        "advertise",
        "newsletter",
        "blog",
        "news",
        "article",
        "guide",
        "about",
        "career",
        "jobs",

        # New
        "investment focus",
        "focus",
        "location",
        "locations",
        "country",
        "city",
        "state",
        "address",
        "headquarters",
        "head office",
        "single-family office",
        "multi-family office",
        "family office services",
        "private investment office",
        "founder office",
        "executive office",
        "learn more",
        "read more",
    }

    BAD_DOMAINS = {
        "swfinstitute.org",
        "fundcomb.com",
        "axial.net",
        "crunchbase.com",
        "pitchbook.com",
        "bloomberg.com",
        "forbes.com",
        "wikipedia.org",
        "unbiased.com",
        "altss.com",
        "pipelineroad.com",
        "investmentnews.com",
        "familyoffices.com",
        "familyofficehub.io",
        "opencorporates.com",
        "zoominfo.com",
        "rocketreach.co",
        "linkedin.com",
        "facebook.com",
        "instagram.com",
    }

    def __init__(self):

        self.search = SearchClient()

        self.cache = {}

    # ----------------------------------------------------------

    def extract_company_names(self, html):

        soup = BeautifulSoup(html, "lxml")

        candidates = []

        selectors = [

            "table td",

            "li",

            "a",

            "h2",

            "h3",

            "strong",

            "b",

        ]

        for selector in selectors:

            for node in soup.select(selector):

                text = node.get_text(" ", strip=True)

                text = re.sub(r"\s+", " ", text)

                if self.is_candidate(text):

                    candidates.append(text)

        return self.remove_duplicates(candidates)

    # ----------------------------------------------------------

    def is_candidate(self, text):

        if not text:

            return False

        text = text.strip()

        if len(text) < 4:

            return False

        if len(text) > 80:

            return False

        lower = text.lower()

        # Reject numbers
        if any(char.isdigit() for char in text):
            return False

        # Reject comma-heavy locations
        if text.count(",") >= 1:
            return False

        # Reject slash labels
        if "/" in text:
            return False

        # Reject all lowercase headings
        if text == text.lower():
            return False

        # Reject ending with country/state abbreviations
        if re.search(r",\s?[A-Z]{2}$", text):
            return False

        # Reject common location suffixes
        LOCATION_SUFFIXES = (
            " usa",
            " us",
            " uk",
            " canada",
            " germany",
            " singapore",
            " switzerland",
            " dubai",
        )

        if lower.endswith(LOCATION_SUFFIXES):
            return False

        STOP_PHRASES = {
            "family office",
            "single family office",
            "multi family office",
            "wealth management",
            "investment office",
            "private investment office",
            "family office services",
        }

        if lower.strip() in STOP_PHRASES:
            return False

        # Reject names ending with common location abbreviations
        if re.search(r"\b(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|IA|ID|IL|IN|KS|KY|LA|MA|MD|ME|MI|MN|MO|MS|MT|NC|ND|NE|NH|NJ|NM|NV|NY|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VA|VT|WA|WI|WV|WY)\b$", text):
            return False

        for word in self.NEGATIVE_WORDS:

            if word in lower:

                return False

        words = re.findall(r"[A-Za-z&'.-]+", text)

        if len(words) < 2:

            return False

        score = 0

        capitals = 0

        for word in words:

            if word[0].isupper():

                capitals += 1

        score += capitals

        for keyword in self.COMPANY_KEYWORDS:

            if keyword in lower:

                score += 3

        if "&" in text:

            score += 1

        if len(words) >= 3:

            score += 1

        if len(words) < 3:
            score -= 1

        return score >= 6

    # ----------------------------------------------------------

    def remove_duplicates(self, names):

        seen = set()

        output = []

        for name in names:

            key = re.sub(r"\s+", " ", name.lower()).strip()

            if key in seen:

                continue

            seen.add(key)

            output.append(name)

        return output

    # ----------------------------------------------------------

    def resolve(self, companies, limit=10):

        resolved = []

        for company in companies[:limit]:

            key = company.lower()

            if key in self.cache:

                resolved.append(self.cache[key])

                continue

            try:

                results = self.search.search(

                    query=f'"{company}" family office official website',

                    max_results=3,

                )

            except Exception:

                continue

            best = self.best_result(results, company)

            if not best:

                continue

            item = {

                "name": company,

                "website": best.get("url", ""),

                "description": best.get("content", ""),

            }

            self.cache[key] = item

            resolved.append(item)

        return resolved

    # ----------------------------------------------------------

    def best_result(self, results, company_name=None):

        if not results:
            return None

        company_words = set()

        if company_name:
            company_words = {
                w.lower()
                for w in re.findall(r"[A-Za-z]+", company_name)
                if len(w) > 2
            }

        best = None
        best_score = float("-inf")

        for result in results:

            url = result.get("url", "")

            if not url:
                continue

            url = url.lower()

            if url.endswith(".pdf"):
                continue

            domain = urlparse(url).netloc.lower()

            if domain.startswith("www."):
                domain = domain[4:]

            score = 0

            # Reject bad domains
            if any(domain.endswith(d) for d in self.BAD_DOMAINS):
                score -= 100

            # Penalize obvious directory/article URLs
            bad_paths = (
                "/directory/",
                "/directories/",
                "/profile/",
                "/profiles/",
                "/article/",
                "/articles/",
                "/news/",
                "/blog/",
                "/wiki/",
            )

            if any(path in url for path in bad_paths):
                score -= 20

            # Reward company name appearing in domain
            for word in company_words:
                if word in domain:
                    score += 8

            # Reward short clean domains
            if url.count("/") <= 3:
                score += 2

            if score > best_score:
                best_score = score
                best = result

        return best