from urllib.parse import urlparse

import requests


class WebsiteValidator:

    BAD_DOMAINS = {
        "linkedin.com",
        "pitchbook.com",
        "crunchbase.com",
        "rocketreach.co",
        "zoominfo.com",
        "fundcomb.com",
        "massinvestordatabase.com",
        "thesisdriven.com",
        "capitalstack.com",
        "altss.com",
        "pipelineroad.com",
        "facebook.com",
        "instagram.com",
        "x.com",
        "twitter.com",
        "youtube.com",
        "wikipedia.org",
        "swfinstitute.org",
    }

    def validate(self, company):

        url = (company.get("website") or "").strip()

        if not url:
            company["validation_status"] = "NO_WEBSITE"
            return company

        domain = self._domain(url)

        if any(domain.endswith(d) for d in self.BAD_DOMAINS):
            company["validation_status"] = "BAD_DOMAIN"
            return company

        try:

            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0"
                },
                allow_redirects=True,
            )

            final_url = response.url

            final_domain = self._domain(final_url)

            if any(final_domain.endswith(d) for d in self.BAD_DOMAINS):
                company["validation_status"] = "BAD_REDIRECT"
                return company

            if response.status_code >= 400:
                company["validation_status"] = "DEAD"
                return company

            company["website"] = final_url
            company["validation_status"] = "VALID"

        except Exception as e:

            company["validation_status"] = "ERROR"
            company["validation_error"] = str(e)

        return company

    def _domain(self, url):

        domain = urlparse(url).netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        return domain