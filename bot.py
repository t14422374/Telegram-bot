import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# --- Get token from environment (Render dashboard → Environment Variables) ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# --- /start command handler ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hey! I’m alive and running on Render 🚀")

# --- message handler (for normal text messages) ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text(f"You said: {user_text}")

# --- main function ---
async def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command + message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot started... Listening for messages.")
    await app.run_polling()

# --- entry point ---
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
