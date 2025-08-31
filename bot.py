from telegram import Update
from telegram.ext import Application, MessageHandler, filters
import requests, os

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def reply(update: Update, context):
    user_message = update.message.text

    # Call OpenRouter API
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    json_data = {
        "model": "openai/gpt-4o-mini",  # change to gpt-oss-120b if you want
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                             headers=headers, json=json_data)

    if response.status_code == 200:
        bot_reply = response.json()["choices"][0]["message"]["content"]
    else:
        bot_reply = f"Error: {response.text}"

    await update.message.reply_text(bot_reply)

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    app.run_polling()

if __name__ == "__main__":
    main()
