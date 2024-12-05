import os
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler
from flask import Flask, request
import matplotlib.pyplot as plt

# تعيين متغيرات البيئة
TOKEN = '8048197051:AAHvIPxu_OtD5G66CgVmJBai4mjFOqDw-cc'  # توكن البوت من تيليجرام
WEBHOOK_URL = 'https://telegram-student-bot-li3t.onrender.com'  # المسار الخاص بك على Render

# Flask app
app = Flask(__name__)

# إعداد Webhook في تيليجرام
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, bot)
    application.process_update(update)
    return 'OK'

# إعداد البوت
application = Application.builder().token(TOKEN).build()

# دالة عرض الدرجات
async def show_grades(update: Update, context):
    student_id = context.args[0]  # رقم الطالب من المدخلات
    student_data = get_student_grades(student_id)
    
    if student_data:
        grades = [grade[1] for grade in student_data]  # درجات الامتحانات
        homework_marks = [grade[2] for grade in student_data]  # درجات أوراق العمل
        average_grade = sum(grades) / len(grades)
        
        subjects = [grade[0] for grade in student_data]
        
        # إنشاء الرسم البياني
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(subjects, grades, color='skyblue', label='Grades')
        ax.bar(subjects, homework_marks, color='lightgreen', label='Homework Marks', alpha=0.6)
        
        ax.set_xlabel('Subjects')
        ax.set_ylabel('Marks')
        ax.set_title(f"Grades and Homework Marks for Student {student_id}")
        ax.legend()
        plt.tight_layout()
        plt.savefig('grades_and_homework_chart.png')
        
        # إرسال الرسالة مع الرسم البياني
        await update.message.reply_text(f"معدل الطالب {student_id}: {average_grade:.2f}")
        await update.message.reply_photo(photo=open('grades_and_homework_chart.png', 'rb'))
        
        await update.message.reply_text(f"يمكنك الوصول إلى رابط الخدمة عبر Render من هنا: {WEBHOOK_URL}")
    else:
        await update.message.reply_text(f"لم يتم العثور على درجات للطالب {student_id}.")

# إضافة الدالة إلى البوت
application.add_handler(CommandHandler("grades", show_grades))

# ربط البوت بـ Webhook
bot = Bot(token=TOKEN)
bot.set_webhook(url=WEBHOOK_URL)

# بدء Flask التطبيق
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
