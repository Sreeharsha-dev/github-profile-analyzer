import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# GitHub token from environment variable
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
