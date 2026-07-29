from app.discovery.base import BaseDiscoverySource
from app.discovery.sources.official_websites import OfficialWebsiteDiscovery


class SearchDiscoverySource(BaseDiscoverySource):

    @property
    def source_name(self):

        return "Search Discovery"

    def discover(self):

        offices = []

        sources = [
            OfficialWebsiteDiscovery(),
        ]

        seen = set()

        for source in sources:

            results = source.discover()

            for office in results:

                key = (
                    office.website.lower().strip()
                    if office.website
                    else office.name.lower().strip()
                )

                if key in seen:
                    continue

                seen.add(key)

                offices.append(office)

        return offices