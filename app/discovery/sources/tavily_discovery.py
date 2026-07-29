from app.discovery.base import BaseDiscoverySource
from app.discovery.search_client import SearchClient
from app.models.family_office import FamilyOffice
from app.discovery.fetcher import WebsiteFetcher
from app.discovery.extractor import CompanyExtractor
from app.discovery.directory_expander import DirectoryExpander


QUERIES = [

    "largest family offices United States",

    "top family offices United States",

    "single family offices Switzerland",

    "family office firms London",

    "family office firms Singapore",

    "family office firms Dubai",

    "independent family offices Germany",

    "family office investment firms Canada",

]


REJECT_DOMAINS = {

    "wikipedia.org",

}


REJECT_WORDS = {

    "what is",

    "difference between",

    "guide",

    "explained",

    "insight",

    "blog",

    "news",

}


class TavilyDiscovery(BaseDiscoverySource):

    def __init__(self):

        self.search = SearchClient()

    @property
    def source_name(self):

        return "Tavily"

    def discover(self):

        fetcher = WebsiteFetcher()
        extractor = CompanyExtractor()
        expander = DirectoryExpander()

        offices = []

        seen_urls = set()
        seen_names = set()

        for query in QUERIES:

            print(f"Searching: {query}")

            results = self.search.search(
                query=query,
                max_results=10,
            )

            for result in results:

                url = result.get("url", "").strip()

                title = result.get("title", "").strip()

                snippet = result.get("content", "").strip()

                if not url:
                    continue

                url_lower = url.lower()
                title_lower = title.lower()
                snippet_lower = snippet.lower()

                if url_lower.endswith(".pdf"):
                    continue

                if any(domain in url_lower for domain in REJECT_DOMAINS):
                    continue

                combined = title_lower + " " + snippet_lower

                if any(word in combined for word in REJECT_WORDS):
                    continue

                if url in seen_urls:
                    continue

                seen_urls.add(url)

                try:
                    html = fetcher.fetch(url)
                    extracted = extractor.extract(html, url)
                except Exception:
                    extracted = {
                        "page_type": "official",
                        "name": title,
                        "description": snippet,
                        "email": None,
                        "phone": None,
                    }

                page_type = extracted.get("page_type", "official")

                if page_type == "reject":
                    continue

                if page_type == "article":
                    continue

                if page_type == "directory":

                    companies = expander.extract_company_names(html)

                    resolved = expander.resolve(
                        companies,
                        limit=10,
                    )

                    for company in resolved:

                        company_name = company["name"].lower()

                        if company_name in seen_names:
                            continue

                        seen_names.add(company_name)

                        office = FamilyOffice.create(
                            name=company["name"],
                            website=company["website"],
                            discovery_source="Tavily",
                        )

                        office.description = company.get(
                            "description",
                            "",
                        )

                        office.verification_status = "Pending"

                        offices.append(office)

                    continue

                office_name = extracted.get("name") or title

                if office_name.lower() in seen_names:
                    continue

                seen_names.add(office_name.lower())

                office = FamilyOffice.create(
                    name=office_name,
                    website=url,
                    discovery_source="Tavily",
                )

                office.description = extracted.get(
                    "description",
                    snippet,
                )

                office.email = extracted.get("email")

                office.phone = extracted.get("phone")

                office.verification_status = "Pending"

                offices.append(office)

        return offices