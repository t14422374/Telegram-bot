import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN is missing! Set it in your environment.")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is missing! Set it in your environment.")

# OpenRouter API call
def query_openrouter(prompt: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://replit.com",  # optional but recommended
        "X-Title": "TelegramBot",              # optional
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4o-mini",  # 🔥 best fast + cheap option
        # Or: "meta-llama/llama-3.1-405b-instruct" for GPT-120B-like giant
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        res_json = response.json()
        return res_json["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error contacting AI: {e}"

# Telegram handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    reply = query_openrouter(user_message)
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

