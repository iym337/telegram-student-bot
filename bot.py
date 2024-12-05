import openpyxl
import matplotlib.pyplot as plt
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# قراءة بيانات الطالب من ملف Excel بناءً على ورقته
def get_student_grades(student_id):
    # تحميل ملف Excel باستخدام المسار الكامل
    file_path = "students_grades.xlsx"  # تأكد من أن الملف في نفس مجلد المشروع أو قدم المسار الكامل
    wb = openpyxl.load_workbook(file_path)
    
    # التحقق إذا كانت ورقة الطالب موجودة
    if str(student_id) in wb.sheetnames:
        sheet = wb[str(student_id)]
    else:
        return None  # ورقة الطالب غير موجودة
    
    # استخراج البيانات من الورقة
    student_data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        student_data.append(row)
    
    return student_data

# عرض الدرجات مع علامات أوراق العمل والرسم البياني
async def show_grades(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    student_id = context.args[0]  # رقم الطالب من المدخلات
    
    # الحصول على درجات الطالب
    student_data = get_student_grades(student_id)
    
    if student_data:
        # حساب المعدل العام للدرجات
        grades = [grade[1] for grade in student_data]  # درجات الامتحانات
        homework_marks = [grade[2] for grade in student_data]  # درجات أوراق العمل
        average_grade = sum(grades) / len(grades)
        
        # رسم بياني للدرجات
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
    else:
        await update.message.reply_text(f"لم يتم العثور على درجات للطالب {student_id}.")

# إعداد البوت
def main():
    # إضافة التوكن هنا
    application = Application.builder().token("8048197051:AAHvIPxu_OtD5G66CgVmJBai4mjFOqDw-cc").build()  # التوكن هنا
    application.add_handler(CommandHandler("grades", show_grades))  # عرض الدرجات مع علامات أوراق العمل

    application.run_polling()

if __name__ == '__main__':
    main()
