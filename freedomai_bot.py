from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import os

app = Flask(__name__)

# توکن رو از متغیر محیطی می‌خونه
token = os.getenv("TELEGRAM_TOKEN")
if not token:
    raise ValueError("توکن تلگرام پیدا نشد! لطفاً متغیر محیطی TELEGRAM_TOKEN رو تنظیم کن.")
application = Application.builder().token(token).build()

@app.route('/')
def home():
    return "Bot is running!"

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "سلام! من بات آزادی مالی برای ایرانی‌ها هستم!\n\n"
        "هدفم اینه که بهت کمک کنم با شرایط ایران به آزادی مالی برسی—جایی که درآمد غیرفعالت هزینه‌هات رو پوشش بده. "
        "برای شروع، از /input استفاده کن!"
    )
    await update.message.reply_text(message)

# دستور /input
async def input_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "لطفاً این اطلاعات رو تو یه پیام (با فاصله) بفرست:\n"
        "۱. پس‌انداز ماهانه (مقدار سرمایه‌گذاری ماهانه به تومان)\n"
        "۲. هزینه ماهانه (درآمد غیرفعال هدف به تومان)\n"
        "۳. ریسک‌پذیری (ریسک‌پذیرم / ریسک‌پذیر نیستم)\n\n"
        "مثال: /input 5000000 10000000 ریسک‌پذیرم"
    )
    await update.message.reply_text(message)

# اضافه کردن دستورات به بات
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("input", input_data))

@app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return '', 200

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(application.initialize())
    port = int(os.environ.get("PORT", 8080))
    webhook_url = "https://freedomai-2025.onrender.com/webhook"
    loop.run_until_complete(application.bot.set_webhook(webhook_url))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()
