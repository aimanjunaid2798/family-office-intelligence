import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

class WebsiteScraper:
    def __init__(self):
        # Professional User-Agent to avoid getting blocked by basic firewalls
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"
        }
        self.timeout = 15

    def scrape(self, url):
        """Main scraping function that extracts title, meta, and combined text from homepage and key subpages."""
        if not url or not url.startswith("http"):
            return {"page_title": "", "meta_description": "", "homepage_text": "", "scraped_emails": []}

        try:
            # Scrape homepage
            response = requests.get(url, headers=self.headers, timeout=self.timeout, verify=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            title = soup.title.string.strip() if soup.title and soup.title.string else ""
            meta_tag = soup.find("meta", attrs={"name": "description"})
            meta = meta_tag["content"].strip() if meta_tag and meta_tag.get("content") else ""

            # Scrape additional key pages (About, Team, Contact) for deeper context
            combined_text = self._extract_clean_text(soup)
            emails = self._extract_emails(soup)

            links = [a.get('href') for a in soup.find_all('a', href=True)]
            subpages_to_scrape = self._filter_key_subpages(url, links)

            for sub_url in subpages_to_scrape[:2]: # Limit to 2 extra pages to save time/bandwidth
                try:
                    time.sleep(1) # Polite scraping delay
                    sub_res = requests.get(sub_url, headers=self.headers, timeout=10, verify=False)
                    if sub_res.status_code == 200:
                        sub_soup = BeautifulSoup(sub_res.text, "html.parser")
                        combined_text += " " + self._extract_clean_text(sub_soup)
                        emails.extend(self._extract_emails(sub_soup))
                except Exception:
                    continue # Skip failed subpages silently

            # Clean and truncate final text for LLM context limits
            final_text = " ".join(combined_text.split())[:8000]

            return {
                "page_title": title,
                "meta_description": meta,
                "homepage_text": final_text,
                "scraped_emails": list(set(emails))
            }

        except Exception as e:
            print(f"Scraping failed for {url}: {str(e)}")
            return {"page_title": "", "meta_description": "", "homepage_text": "", "scraped_emails": []}

    def _extract_clean_text(self, soup):
        # Remove scripts, styles, navs, and footers to keep only content
        for element in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            element.decompose()
        return soup.get_text(separator=" ", strip=True)

    def _filter_key_subpages(self, base_url, links):
        key_keywords = ["about", "team", "who-we-are", "contact", "firm", "company"]
        valid_links = []
        base_domain = urlparse(base_url).netloc

        for link in set(links):
            full_url = urljoin(base_url, link)
            if urlparse(full_url).netloc == base_domain:
                if any(kw in link.lower() for kw in key_keywords):
                    valid_links.append(full_url)
        return valid_links

    def _extract_emails(self, soup):
        import re
        text = soup.get_text()
        emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
        return [email for email in emails if not email.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg'))]