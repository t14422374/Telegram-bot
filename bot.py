import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# -------------------------------------------------
# Logging setup
# -------------------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Check if tokens are present
if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN is missing! Please set it in Render > Environment.")
else:
    print(f"✅ Loaded TELEGRAM_TOKEN: {TELEGRAM_TOKEN[:10]}...")

if not OPENROUTER_API_KEY:
    raise ValueError("❌ OPENROUTER_API_KEY is missing! Please set it in Render > Environment.")
else:
    print(f"✅ Loaded OPENROUTER_API_KEY (first 8 chars): {OPENROUTER_API_KEY[:8]}...")

# -------------------------------------------------
# OpenRouter API call
# -------------------------------------------------
def query_openrouter(prompt: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "applicatio

