# workers/telegram_bot.py
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Ваш ID

application = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🕷️ SPIDER Bot готов. Используй /scan <цель>")

async def scan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = " ".join(context.args)
    if not target:
        await update.message.reply_text("Укажите цель: /scan email@example.com")
        return
    # Запуск сканирования
    run_osint_scan.delay(target, ["all"], True)
    await update.message.reply_text(f"Сканирование запущено: {target}")

def start_bot():
    global application
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("scan", scan_command))
    application.run_polling()

@celery.task
def notify_telegram(message: str):
    if application:
        asyncio.create_task(application.bot.send_message(chat_id=CHAT_ID, text=message))