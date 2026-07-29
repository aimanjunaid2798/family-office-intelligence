import os
import time
from tavily import TavilyClient
from dotenv import load_dotenv

class SearchClient:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            print("[Warning] TAVILY_API_KEY is missing from your environment variables!")
        self.client = TavilyClient(api_key=api_key)

    def search(self, query, max_results=4):
        # SAFE WRAPPER: 2 attempts retry mechanism network exceptions handle karne ke liye
        for attempt in range(2):
            try:
                response = self.client.search(
                    query=query,
                    max_results=max_results
                )
                
                # Agar Tavily directly list return karta hai, toh use dict structure mein convert kar dein
                if isinstance(response, list):
                    return {"results": response}
                
                return response
                
            except Exception as e:
                print(f"\n   [Warning] Tavily API connection glitch on attempt {attempt+1}: {e}")
                if attempt < 1:
                    print("   Retrying in 2 seconds...")
                    time.sleep(2)  # Short cooling period before retry
                else:
                    print("   [Warning] Max retries exhausted for this query. Skipping gracefully to prevent pipeline crash...")
        
        # Safe fallback dictionary taake website_enricher.py crash na ho
        return {"results": []}