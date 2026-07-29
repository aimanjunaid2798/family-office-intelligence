from app.discovery.sources.tavily_discovery import TavilyDiscovery
from app.discovery.validator import FamilyOfficeValidator


class DiscoveryManager:

    def __init__(self):

        self.discovery = TavilyDiscovery()
        self.validator = FamilyOfficeValidator()

    def discover(self):

        print("\nStarting Family Office Discovery...\n")

        candidates = self.discovery.discover()

        print(f"\nDiscovered {len(candidates)} candidate offices\n")

        validated = []

        seen = set()

        for office in candidates:

            if not office.name:
                continue

            key = (
                (office.website or "").strip().lower(),
                (office.name or "").strip().lower(),
            )

            if key in seen:
                continue

            seen.add(key)

            try:

                validated.append(
                    self.validator.validate(office)
                )

            except Exception as e:

                office.verification_status = "Rejected"
                office.verification_notes = str(e)

                validated.append(office)

        print(f"Validated {len(validated)} offices\n")

        return validated