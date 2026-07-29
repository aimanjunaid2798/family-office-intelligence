from urllib.parse import urljoin

from bs4 import BeautifulSoup


class LinkExtractor:

    def extract_links(self, html: str, base_url: str):

        soup = BeautifulSoup(html, "lxml")

        links = set()

        for tag in soup.find_all("a", href=True):

            href = tag["href"].strip()

            if (
                not href
                or href.startswith("#")
                or href.startswith("mailto:")
                or href.startswith("tel:")
                or href.startswith("javascript:")
            ):
                continue

            absolute = urljoin(base_url, href)

            if absolute.startswith("http"):
                links.add(absolute)

        return sorted(links)