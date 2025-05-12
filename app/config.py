import os
from dotenv import load_dotenv

# Force reload environment variables
load_dotenv(override=True)

DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_REAL_MODEL = os.getenv("USE_REAL_MODEL", "false").lower() == "true"