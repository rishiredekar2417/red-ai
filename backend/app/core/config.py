from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4000"))
PROVIDER = os.getenv("PROVIDER", "openai")

# Application Configuration
APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")
ENVIRONMENT = os.getenv("ENVIRONMENT")
LOG_LEVEL = os.getenv("LOG_LEVEL")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")