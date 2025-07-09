import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
REDIS_URL = os.getenv('REDIS_URL')
