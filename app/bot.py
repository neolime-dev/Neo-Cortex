import os
import logging
import requests
import hashlib
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

# --- Configuration ---
# No Pi, criaremos um .env local ou passaremos variaveis de ambiente
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_ID = os.getenv("ALLOWED_USER_ID")
API_URL = "http://localhost:8000/ingest/" # Localhost pois roda no mesmo Pi

# Logging Setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def is_authorized(user_id):
    if not ALLOWED_USER_ID:
        return False
    return str(user_id) == str(ALLOWED_USER_ID)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        return
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🧠 Neo-Cortex Online. I am the Brain now."
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        return

    text = update.message.text
    message_id = update.message.message_id
    
    # Cria ID unico baseado na mensagem do telegram
    source_id = f"telegram-{message_id}"

    payload = {
        "content": f"[Mobile] {text}",
        "source": "telegram",
        "source_id": source_id,
        "status": "pending",
        "is_pinned": False
    }

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        await update.message.reply_text("✅ Saved to Cortex.")
    except Exception as e:
        logging.error(f"API Error: {e}")
        await update.message.reply_text(f"❌ Brain Error: {e}")

def main():
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set")
        return

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    
    print("Neo-Cortex Bot running...")
    application.run_polling()

if __name__ == '__main__':
    main()
