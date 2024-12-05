import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from flask import Flask, request
from waitress import serve

# إعداد Flask
app = Flask(__name__)

# إعداد تسجيل الدخول
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# توكن البوت
TELEGRAM_API_TOKEN = '8048197051:AAHvIPxu_OtD5G66CgVmJBai4mjFOqDw-cc'
WEBHOOK_URL = 'https://telegram-student-bot-li3t.onrender.com'  # الرابط الخاص بك على Render

# إعداد الديسباتشر والبوت
updater = Updater(token=TELEGRAM_API_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# وظيفة بدء التفاعل مع البوت
def start(update: Update, context: CallbackContext):
    update.message.reply_text("مرحباً! أنا بوت الطالب.")

# إضافة معالج للأوامر
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# إعداد Webhook
@app.route('/' + TELEGRAM_API_TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, updater.bot)
    dispatcher.process_update(update)
    return 'OK', 200

# بدء تشغيل Flask باستخدام Waitress
if __name__ == '__main__':
    # لتشغيل البوت على Webhook
    serve(app, host='0.0.0.0', port=5000)
