from app.discovery.llm_classifier import LLMClassifier

classifier = LLMClassifier(
    model="qwen2.5:7b",
    workers=5,
)

classifier.classify(
    input_csv="datasets/raw/discovered_family_offices.csv",
    authentic_csv="datasets/processed/authentic_family_offices.csv",
    review_csv="datasets/processed/review_family_offices.csv",
    rejected_csv="datasets/processed/rejected_family_offices.csv",
)