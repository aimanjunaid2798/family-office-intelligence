import re
from urllib.parse import urljoin, urlparse

from app.discovery.base import BaseDiscoverySource
from app.discovery.extractor import CompanyExtractor
from app.discovery.fetcher import WebsiteFetcher
from app.discovery.parser import LinkExtractor
from app.discovery.sources.discovery_sources import DISCOVERY_SOURCES
from app.models.family_office import FamilyOffice


class OfficialWebsiteDiscovery(BaseDiscoverySource):

    FAMILY_OFFICE_PATTERN = re.compile(
        r"(family office|wealth|capital|partners|investments|asset)",
        re.IGNORECASE,
    )

    def __init__(self):

        self.fetcher = WebsiteFetcher()
        self.parser = LinkExtractor()
        self.extractor = CompanyExtractor()

    @property
    def source_name(self):

        return "Official Websites"

    def discover(self):

        offices = []
        visited = set()

        for source in DISCOVERY_SOURCES:

            try:

                html = self.fetcher.fetch(source)

            except Exception:
                continue

            links = self.parser.extract_links(
                html,
                source,
            )

            for link in links:

                normalized = self.normalize(link)

                if normalized in visited:
                    continue

                visited.add(normalized)

                if not self.looks_like_candidate(link):
                    continue

                try:

                    page = self.fetcher.fetch(link)

                except Exception:
                    continue

                data = self.extractor.extract(page)

                if not data["name"]:
                    continue

                office = FamilyOffice.create(
                    name=data["name"],
                    website=normalized,
                    discovery_source=source,
                )

                office.description = data["description"]
                office.email = data["email"]
                office.phone = data["phone"]

                offices.append(office)

        return offices

    def looks_like_candidate(self, url):

        text = url.lower()

        return bool(
            self.FAMILY_OFFICE_PATTERN.search(text)
        )

    def normalize(self, url):

        parsed = urlparse(url)

        return parsed.scheme + "://" + parsed.netloc