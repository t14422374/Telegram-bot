import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your-telegram-token-here")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your-openrouter-key-here")

# 1. /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello 👋! I’m your AI bot, powered by OpenRouter 🤖")

# 2. Handle normal messages with AI response
async def chat_with_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-4o-mini",  # or "gpt-oss-120b" if you prefer
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant in Telegram."},
                    {"role": "user", "content": user_message}
                ]
            }
        )

        data = response.json()
        ai_reply = data["choices"][0]["message"]["content"]

    except Exception as e:
        ai_reply = f"⚠️ Error talking to AI: {str(e)}"

    await update.message.reply_text(ai_reply)

# Main app
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))

    # Text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_ai))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
