import csv
import logging
import json
from app.discovery.ollama_client import OllamaClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SYSTEM_VALIDATION_PROMPT = """
You are an expert financial data auditor specializing in institutional investment frameworks and Family Offices.
Your task is to validate a candidate name and web text to filter out web extraction garbage and accurately classify Single-Family Offices (SFO).

Analyze the input data and return a JSON object with exactly these keys:
{
  "status": "VERIFIED" or "REJECTED",
  "score": <float between 0.0 and 100.0 based on evidence strength, domain validity, and exclusive indicators>,
  "reason": "A precise 1-sentence explanation of the validation outcome"
}

Strict Rules:
1. ENTITY VALIDATION: If the name is web garbage, a button, navigation menu, or blog topic (e.g., 'FOLLOW US ON SOCIAL MEDIA', 'Direct Investments', 'Regional Breakdown', 'Trust & Security'), you MUST set status to 'REJECTED'.
2. PLATFORM FILTER: If the company is a multi-client generic financial advisor, broker-dealer, or a directory link, set status to 'REJECTED'.
3. LEGACY RECOVERY: If the name is a known authentic private single-family wealth controller or institutional private management asset house (e.g., 'Soros Fund Management', 'JAB Holding Company'), you MUST set status to 'VERIFIED' and provide an evidence score above 90.0.
4. EVIDENCE SCORING: Do NOT give a flat threshold score (like 85.0) to everything. Vary the score strictly based on the explicit presence of family office indicators and domain quality.
"""

class AssessmentPipelineProcessor:
    def __init__(self, input_csv_path, output_csv_path):
        self.input_path = input_csv_path
        self.output_path = output_csv_path
        # Core model client activation using your exact implementation structure
        self.llm = OllamaClient(model="qwen2.5:7b")

    def run(self):
        logging.info("Starting automated LLM-driven entity validation...")
        
        try:
            with open(self.input_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                fieldnames = list(reader.fieldnames) if reader.fieldnames else []
                rows = list(reader)
        except Exception as e:
            logging.error(f"Error reading source data: {e}")
            return

        # Explicitly tracking clean evaluation schema
        for col in ['final_status', 'final_score', 'validation_notes']:
            if col not in fieldnames:
                fieldnames.append(col)

        verified_count = 0
        rejected_count = 0

        for idx, row in enumerate(rows):
            # Extract standard fields based on pipeline patterns
            name = row.get('name', row.get('company_name', '')).strip()
            website = row.get('website', row.get('domain', '')).strip()
            homepage_text = row.get('homepage_text', row.get('scraped_content', '')).strip()
            
            user_prompt = f"Entity Name: {name}\nWebsite: {website}\nScraped Snippet: {homepage_text[:600]}"
            
            try:
                # Actual live inference using Qwen 2.5 local agent
                llm_response = self.llm.classify(
                    user_prompt=user_prompt,
                    system_prompt=SYSTEM_VALIDATION_PROMPT,
                    temperature=0
                )
                
                status = llm_response.get('status', 'REJECTED').strip().capitalize()
                score = llm_response.get('score', 0.0)
                reason = llm_response.get('reason', 'Validation complete.')
                
            except Exception as e:
                logging.warning(f"LLM parsing failed for row {idx+1} ({name}), using defensive fallback: {e}")
                status, score, reason = 'Rejected', 0.0, "Execution bypass due to parse exceptions."

            row['final_status'] = status
            row['final_score'] = str(score)
            row['validation_notes'] = reason
            
            if status == 'Verified':
                verified_count += 1
            else:
                rejected_count += 1
                
            if (idx + 1) % 10 == 0:
                logging.info(f"Processed {idx + 1}/{len(rows)} records through Qwen Model...")

        try:
            with open(self.output_path, mode='w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            logging.info(f"Validation Complete! Real Verified: {verified_count} | Real Rejected: {rejected_count}")
            logging.info(f"Clean evaluation dataset saved to: {self.output_path}")
        except Exception as e:
            logging.error(f"Error compiling clean dataset: {e}")