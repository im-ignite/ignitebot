import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot token
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Admin IDs as a list of integers
ADMIN_IDS = [int(id.strip()) for id in os.getenv('ADMIN_IDS', '').split(',')]

