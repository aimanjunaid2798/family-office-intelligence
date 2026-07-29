from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# ==============================
# Project Paths
# ==============================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATASET_DIR = PROJECT_ROOT / "datasets" / "raw"
PROCESSED_DATASET_DIR = PROJECT_ROOT / "datasets" / "processed"
VALIDATED_DATASET_DIR = PROJECT_ROOT / "datasets" / "validated"

DISCOVERED_CSV = RAW_DATASET_DIR / "discovered_family_offices.csv"


# ==============================
# Network Settings
# ==============================

DISCOVERY_SOURCES = [
    "https://familyofficehub.io/",
    "https://www.fintrx.com/",
    "https://familyoffices.com/",
]

DISCOVERY_QUERIES = [
    "family office",
    "single family office",
    "multi family office",
]

REQUEST_TIMEOUT = 30

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/138.0 Safari/537.36"
)


# ==============================
# Retry Settings
# ==============================

MAX_RETRIES = 3
RETRY_DELAY = 2