import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TESSERACT_PATH = os.getenv("TESSERACT_PATH")
POPPLER_PATH = os.environ.get("POPPLER_PATH")
