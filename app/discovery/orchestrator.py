import csv
import time
from app.discovery.website_enricher import WebsiteEnricher
from app.discovery.website_scraper import WebsiteScraper
from app.discovery.final_verifier import FinalVerifier
import urllib3

# Suppress insecure request warnings for scraping
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DiscoveryOrchestrator:
    def __init__(self, input_csv, output_csv):
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.enricher = WebsiteEnricher()
        self.scraper = WebsiteScraper()
        self.verifier = FinalVerifier()

    def run(self):
        print(f"Loading data from {self.input_csv} (using Hybrid Credit-Saver Parser)...")
        
        try:
            with open(self.input_csv, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                rows = list(reader)
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            return

        total_rows = len(rows)
        print(f"Found {total_rows} total records to inspect.")

        results = []
        verified_count = 0
        review_count = 0
        rejected_count = 0

        for index, row in enumerate(rows, start=1):
            name = row.get('name', 'Unknown')
            init_status = str(row.get('verification_status', '')).strip().upper()
            
            print(f"[{index}/{total_rows}] Analyzing: {name} (Initial Status: {row.get('verification_status')})")
            
            # HYBRID ROUTING MATRIX
            should_process = True
            
            if init_status == "REJECTED":
                # Check if it has a valid existing website or embedded URL inside the description text
                existing_web = (row.get("website") or "").strip()
                desc_text = row.get("description", "") or ""
                extracted_url = self.enricher.extract_url_from_text(f"{existing_web} {desc_text}")
                
                if extracted_url and self.enricher.looks_official(extracted_url):
                    # Found a hidden asset! Process it using FREE local resources (Scraper + Local LLM)
                    row["website"] = extracted_url
                    row["website_status"] = "EXISTING"
                    print(f"   -> [Gems Recovery]: Recovered domain '{extracted_url}' from text. Scraping with zero-credit cost.")
                else:
                    # Absolute blind spot with no links. Skip search to protect Tavily credits.
                    row["final_decision"] = "NOT_FAMILY_OFFICE"
                    row["reason"] = "Skipped: Pre-rejected in discovery phase with no local domain signatures available."
                    row["page_title"] = ""
                    row["meta_description"] = ""
                    row["homepage_text"] = ""
                    row["evidence_score"] = 0
                    row["llm_confidence"] = 0.0
                    should_process = False
                    rejected_count += 1
                    results.append(row)
                    continue

            if should_process:
                # Step 1: Enrich / Extract Website (Only calls Tavily if status wasn't forced to EXISTING above)
                company = self.enricher.enrich(row)
                
                # Step 2: Scrape content using free HTTP client
                if company.get("website") and company.get("website_status") in ["FOUND", "EXISTING", "REVIEW"]:
                    scraped_data = self.scraper.scrape(company["website"])
                    company.update(scraped_data)
                    
                    # Step 3: Final Verification via local rules + local LLM context checking
                    company = self.verifier.verify(company)
                else:
                    company["final_decision"] = "REVIEW"
                    company["reason"] = "No corporate website resolved during enrichment."
                    company["page_title"] = ""
                    company["meta_description"] = ""
                    company["homepage_text"] = ""
                    company["evidence_score"] = 0
                    company["llm_confidence"] = 0.0

                # Metric Logging
                decision = company.get("final_decision")
                if decision == "VERIFIED_FAMILY_OFFICE":
                    verified_count += 1
                    print(f"   -> [RESULT]: SUCCESS - Verified Family Office!")
                elif decision == "REVIEW":
                    review_count += 1
                    print(f"   -> [RESULT]: Pushed to manual REVIEW pool.")
                else:
                    rejected_count += 1
                    print(f"   -> [RESULT]: REJECTED.")

                results.append(company)
                
                # Tiny safe delay between active network scrapes
                time.sleep(0.5)

        print("\nProcessing complete. Exiting compilation engine...")
        self.save_results(results, fieldnames)
        
        print(f"\n--- Smart Hybrid Pipeline Summary ---")
        print(f"Total Inspected: {len(results)}")
        print(f"Verified Family Offices: {verified_count}")
        print(f"Sent to Review Pool: {review_count}")
        print(f"Final Rejections: {rejected_count}")

    def save_results(self, results, original_fields):
        if not results:
            return
        all_keys = set()
        for r in results:
            all_keys.update(r.keys())
        
        priority_cols = ["id", "name", "website", "final_decision", "llm_confidence", "reason", "evidence_score"]
        final_fields = [col for col in priority_cols if col in all_keys]
        for col in all_keys:
            if col not in final_fields:
                final_fields.append(col)

        try:
            with open(self.output_csv, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=final_fields)
                writer.writeheader()
                for row in results:
                    complete_row = {k: row.get(k, "") for k in final_fields}
                    writer.writerow(complete_row)
            print(f"Data successfully saved to {self.output_csv}")
        except Exception as e:
            print(f"Error saving output CSV: {e}")