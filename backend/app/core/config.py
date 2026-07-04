from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Application Configuration
APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")
ENVIRONMENT = os.getenv("ENVIRONMENT")
LOG_LEVEL = os.getenv("LOG_LEVEL")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")