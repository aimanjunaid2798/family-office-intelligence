import csv
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from app.discovery.ollama_client import OllamaClient
from app.discovery.prompts import build_prompt


class LLMClassifier:

    def __init__(
        self,
        model="qwen2.5:7b",
        workers=5,
        cache_file="cache/classifier_cache.json",
    ):
        self.client = OllamaClient(model=model)
        self.workers = workers

        self.cache_path = Path(cache_file)
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)

        if self.cache_path.exists():
            with open(self.cache_path, encoding="utf-8") as f:
                self.cache = json.load(f)
        else:
            self.cache = {}

    # -------------------------------------------------------------

    def save_cache(self):

        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(
                self.cache,
                f,
                indent=2,
                ensure_ascii=False,
            )

    # -------------------------------------------------------------

    def load_csv(self, path):

        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    # -------------------------------------------------------------

    def write_csv(self, path, rows):

        if not rows:
            print(f"No rows -> {path}")
            return

        Path(path).parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", newline="", encoding="utf-8") as f:

            writer = csv.DictWriter(
                f,
                fieldnames=rows[0].keys(),
            )

            writer.writeheader()
            writer.writerows(rows)

    # -------------------------------------------------------------

    def classify_row(self, row):

        key = (
            row.get("name", "")
            + row.get("website", "")
            + row.get("description", "")
        )

        if key in self.cache:
            result = self.cache[key]
            row.update(result)
            return row

        prompt = build_prompt(row)

        for _ in range(3):

            try:

                result = self.client.classify(prompt)

                if "decision" not in result:
                    raise Exception("Missing decision")

                row.update(result)

                self.cache[key] = result

                return row

            except Exception:
                pass

        row["decision"] = "review"
        row["company_type"] = "Unknown"
        row["confidence"] = 0
        row["reason"] = "LLM failed after retries"

        return row

    # -------------------------------------------------------------

    def classify(
        self,
        input_csv,
        authentic_csv,
        review_csv,
        rejected_csv,
    ):

        rows = self.load_csv(input_csv)

        authentic = []
        review = []
        rejected = []

        futures = []

        with ThreadPoolExecutor(
            max_workers=self.workers
        ) as executor:

            for row in rows:
                futures.append(
                    executor.submit(
                        self.classify_row,
                        row,
                    )
                )

            total = len(futures)

            for i, future in enumerate(
                as_completed(futures),
                start=1,
            ):

                row = future.result()

                decision = (
                    row.get("decision", "")
                    .strip()
                    .lower()
                )

                if decision == "authentic":
                    authentic.append(row)

                elif decision == "reject":
                    rejected.append(row)

                else:
                    review.append(row)

                print(
                    f"[{i}/{total}] "
                    f"{row.get('name','')} -> {decision}"
                )

        self.save_cache()

        self.write_csv(authentic_csv, authentic)
        self.write_csv(review_csv, review)
        self.write_csv(rejected_csv, rejected)

        print("\n========== DONE ==========")
        print("Authentic :", len(authentic))
        print("Review    :", len(review))
        print("Rejected  :", len(rejected))
        print("==========================")