import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup


class CompanyExtractor:

    EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    PHONE_PATTERN = r"\+?\d[\d\s().-]{7,}\d"

    ARTICLE_KEYWORDS = {
        "what is",
        "difference between",
        "guide",
        "blog",
        "insight",
        "article",
        "news",
        "explained",
        "understanding",
    }

    DIRECTORY_KEYWORDS = {
        "family offices",
        "largest family offices",
        "top family offices",
        "list of family offices",
        "directory",
        "companies",
        "members",
    }

    REJECT_DOMAINS = {
        "wikipedia.org",
    }

    def extract(self, html: str, url: str = "") -> dict:

        soup = BeautifulSoup(html, "lxml")
        text = soup.get_text(" ", strip=True)

        title = self.company_name(soup)
        description = self.description(soup)

        page_type = self.detect_page_type(
            title,
            description,
            url,
        )

        return {
            "name": title,
            "description": description,
            "email": self.email(text),
            "phone": self.phone(text),
            "page_type": page_type,
        }

    def company_name(self, soup):

        if soup.title and soup.title.text:

            title = soup.title.text.strip()

            for separator in ["|", "-", "•"]:
                if separator in title:
                    title = title.split(separator)[0].strip()

            return title

        h1 = soup.find("h1")
        if h1:
            return h1.get_text(strip=True)

        return ""

    def description(self, soup):

        meta = soup.find("meta", attrs={"name": "description"})

        if meta:
            return meta.get("content", "").strip()

        return ""

    def email(self, text):

        matches = re.findall(self.EMAIL_PATTERN, text)

        return matches[0] if matches else None

    def phone(self, text):

        matches = re.findall(self.PHONE_PATTERN, text)

        return matches[0] if matches else None

    def detect_page_type(
        self,
        title,
        description,
        url,
    ):

        url_lower = url.lower()
        title_lower = title.lower()
        desc_lower = description.lower()

        # Reject PDFs
        if url_lower.endswith(".pdf"):
            return "reject"

        # Reject known domains
        domain = urlparse(url_lower).netloc

        for bad in self.REJECT_DOMAINS:
            if bad in domain:
                return "reject"

        combined = (
            title_lower +
            " " +
            desc_lower
        )

        # Directory page
        for keyword in self.DIRECTORY_KEYWORDS:
            if keyword in combined:
                return "directory"

        # Article page
        for keyword in self.ARTICLE_KEYWORDS:
            if keyword in combined:
                return "article"

        # Looks like company website
        return "official"