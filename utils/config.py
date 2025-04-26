import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")