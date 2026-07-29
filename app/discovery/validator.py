import re
from urllib.parse import urlparse

import requests

from app.models.family_office import FamilyOffice

BLACKLIST_DOMAINS = {
    "linkedin.com",
    "facebook.com",
    "instagram.com",
    "twitter.com",
    "x.com",
    "youtube.com",
    "wikipedia.org",
    "fundcomb.com",
    "axial.net",
}

GOOD_KEYWORDS = {
    "family office",
    "single family office",
    "multi family office",
    "wealth management",
    "family wealth",
    "investment office",
    "private capital",
    "asset management",
    "capital management",
}

BAD_KEYWORDS = {
    "blog",
    "article",
    "guide",
    "news",
    "explained",
    "learn",
    "tutorial",
    "compare",
    "comparison",
    "definition",
    "meaning",
    "history",
}


class FamilyOfficeValidator:

    EMAIL_PATTERN = (
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    )

    def validate(self, office: FamilyOffice) -> FamilyOffice:

        office.verification_status = "Pending"

        if not office.website:
            office.verification_status = "Rejected"
            office.verification_notes = "Missing website"
            return office

        normalized = self.normalize(office.website)
        domain = urlparse(normalized).netloc

        if any(domain.endswith(d) for d in BLACKLIST_DOMAINS):
            office.verification_status = "Rejected"
            office.verification_notes = "Directory / Social website"
            return office

        if not self.website_alive(office.website):
            office.verification_status = "Rejected"
            office.verification_notes = "Website unreachable"
            return office

        if office.email:
            if (
                not re.fullmatch(self.EMAIL_PATTERN, office.email)
                or office.email.lower().endswith(
                    (
                        ".png",
                        ".jpg",
                        ".jpeg",
                        ".svg",
                        ".gif",
                        ".webp",
                    )
                )
            ):
                office.email = None

        score = 0

        # Website reachable
        score += 3

        if office.email:
            score += 1

            try:
                email_domain = office.email.split("@")[-1].lower()

                if domain.endswith(email_domain):
                    score += 2

            except Exception:
                pass

        if office.phone:
            score += 1

        combined = " ".join(
            filter(
                None,
                [
                    office.name,
                    office.description,
                    office.website,
                ],
            )
        ).lower()

        if any(keyword in combined for keyword in GOOD_KEYWORDS):
            score += 3

        if any(keyword in combined for keyword in BAD_KEYWORDS):
            score -= 2

        if score >= 6:
            office.verification_status = "Verified"

        elif score >= 4:
            office.verification_status = "Needs Review"

        else:
            office.verification_status = "Rejected"

        office.verification_notes = (
            f"Validation score: {score}"
        )

        return office

    def website_alive(self, url: str) -> bool:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        try:

            response = requests.get(
                url,
                timeout=10,
                headers=headers,
                allow_redirects=True,
                stream=True,
            )

            status = response.status_code
            response.close()

            return status in (200, 301, 302, 403)

        except Exception:
            return False

    def normalize(self, url: str) -> str:

        parsed = urlparse(url)

        domain = parsed.netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        return f"{parsed.scheme}://{domain}"