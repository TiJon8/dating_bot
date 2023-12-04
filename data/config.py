import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = str(os.getenv("TOKEN"))
PRIVATE_CHANNEL_ID = int(os.getenv("PRIVATE_CHANNEL_ID"))
BOT_ID = int(os.getenv("BOT_ID"))
ADMINS = os.getenv("ADMINS")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")