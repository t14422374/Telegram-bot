import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
import requests, os

# Setup logging so messages appear in Render logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def reply(update: Update, context):
    user_message = update.message.text
    logger.info(f"User ({update.effective_user.id}): {user_message}")

    # Call OpenRouter API
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    json_data = {
        "model": "openai/gpt-4o-mini",  # or "gpt-oss-120b"
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=json_data
        )

        if response.status_code == 200:
            bot_reply = response.json()["choices"][0]["message"]["content"]
        else:
            bot_reply = f"Error: {response.text}"

    except Exception as e:
        bot_reply = f"Exception: {e}"
        logger.error(f"Error from OpenRouter: {e}")

    logger.info(f"Bot reply: {bot_reply}")
    await update.message.reply_text(bot_reply)

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    app.run_polling()

if __name__ == "__main__":
    main()
