from bs4 import BeautifulSoup


class FamilyOfficeClassifier:

    KEYWORDS = [
        "family office",
        "single family office",
        "multi family office",
        "wealth management",
        "private investment",
        "family capital",
    ]

    def is_family_office(self, html: str) -> bool:

        text = BeautifulSoup(html, "lxml").get_text(" ", strip=True).lower()

        return any(keyword in text for keyword in self.KEYWORDS)