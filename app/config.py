import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
HF_API_KEY = os.getenv("HF_API_KEY", "").strip()
FORCE_DEMO = os.getenv("DEMO_MODE", "0") == "1"

# Text AI is live only when a key exists and demo mode is not forced.
TEXT_LIVE = bool(GEMINI_API_KEY) and not FORCE_DEMO
NUM_PANELS = 5
