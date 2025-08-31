import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# 🔑 Your keys
OPENROUTER_API_KEY = "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"
TELEGRAM_BOT_TOKEN = "8289027938:AAEzzJgMUwJPg1dgdIg6PaYu2m8bMQpJQjU"

# 🔮 Ask GPT-OSS-120B via OpenRouter
def ask_gpt(message: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {"role": "system", "content": "You are a helpful and fun AI assistant."},
            {"role": "user", "content": message},
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Error: {e}\nResponse: {response.text}"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey 👋 I’m your GPT-OSS AI bot. Just send me a message!")

# Handle normal messages
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    reply = ask_gpt(user_message)
    await update.message.reply_text(reply)

# Main bot runner
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    main()
