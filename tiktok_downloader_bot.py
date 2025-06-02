import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from TikTokApi import TikTokApi
import re
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

api = TikTokApi.get_instance(use_selenium=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("������� ������ �� TikTok �����, � � ������ ���!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    tiktok_url_pattern = r'https?://(vm\.tiktok\.com|www\.tiktok\.com)/[a-zA-Z0-9@/_]+'
    
    if re.match(tiktok_url_pattern, message_text):
        try:
            await update.message.reply_text("�������� �����...")
            video_data = api.video(url=message_text)
            video_bytes = video_data.bytes()
            temp_file = "temp_video.mp4"
            with open(temp_file, "wb") as f:
                f.write(video_bytes)
            with open(temp_file, "rb") as f:
                await update.message.reply_video(video=f, caption="��� ���� �����!")
            os.remove(temp_file)
        except Exception as e:
            logger.error(f"������: {e}")
            await update.message.reply_text("������! ������� ������ ��� �������� �����.")
    else:
        await update.message.reply_text("������� ������ �� TikTok �����.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"������: {context.error}")
    await update.message.reply_text("���-�� ����� �� ���. �������� ��� ���.")

def main():
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()