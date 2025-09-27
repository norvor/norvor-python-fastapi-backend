import os
from dotenv import load_dotenv

# This line loads the environment variables from your .env file
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    # Add other application-wide settings here in the future
    # For example: API_V1_STR: str = "/api/v1"

settings = Settings()