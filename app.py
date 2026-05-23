from flask import Flask, render_template, request
from PyPDF2 import PdfReader
from docx import Document
import webbrowser

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB


# 🛡️ فحص الأمان
def security_basic(code):
    warnings = []

    if "eval" in code:
        warnings.append("⚠️ استخدام eval خطر")

    if "exec" in code:
        warnings.append("⚠️ استخدام exec خطر")

    if "os.system" in code:
        warnings.append("⚠️ تنفيذ أوامر نظام")

    if "subprocess" in code:
        warnings.append("⚠️ subprocess قد يكون خطر")

    return "\n".join(warnings) if warnings else "✅ لا يوجد خطر واضح"


# 🤖 تحليل ذكي محلي بدون Ollama
def ai_analyze(code):

    lines = code.splitlines()

    result = []

    # 📏 إحصائيات
    result.append(f" عدد الأسطر: {len(lines)}")
    result.append(f" عدد الكلمات: {len(code.split())}")
    result.append(f" عدد الأحرف: {len(code)}")

    # 📦 تحليل المكونات
    functions = code.count("def ")
    classes = code.count("class ")
    loops = code.count("for ") + code.count("while ")
    conditions = code.count("if ")

    result.append("\n مكونات الكود:")
    result.append(f"• الدوال: {functions}")
    result.append(f"• الكلاسات: {classes}")
    result.append(f"• الحلقات: {loops}")
    result.append(f"• الشروط: {conditions}")

    # 🧠 تحليل ذكي
    result.append("\n التحليل الذكي:")

    if functions == 0:
        result.append("• يفضل تقسيم الكود إلى دوال")

    if loops > 3:
        result.append("• يوجد عدد حلقات كبير قد يؤثر على الأداء")

    if "try" not in code:
        result.append("• لا يوجد try/except لمعالجة الأخطاء")

    if "input(" in code:
        result.append("• تحقق من حماية المدخلات")

    if "print" in code:
        result.append("• يستخدم أوامر الطباعة")

    if "import *" in code:
        result.append("• يفضل عدم استخدام import *")

    # 🔐 التحليل الأمني
    result.append("\n🔐 التحليل الأمني:")

    if "eval" in code:
        result.append("• eval قد يسمح بتنفيذ أكواد خطيرة")

    if "exec" in code:
        result.append("• exec قد يسبب ثغرات أمنية")

    if "os.system" in code:
        result.append("• تنفيذ أوامر النظام قد يكون خطر")

    if "subprocess" in code:
        result.append("• subprocess يحتاج تحقق أمني")

    # ⭐ التقييم
    score = 10

    if functions == 0:
        score -= 2

    if "eval" in code:
        score -= 3

    if "exec" in code:
        score -= 2

    if loops > 5:
        score -= 1

    if score < 1:
        score = 1

    result.append(f"\n⭐ تقييم الكود: {score}/10")

    return "\n".join(result)


@app.route("/", methods=["GET", "POST"])
def index():

    code = ""
    ai = ""
    security = ""

    if request.method == "POST":

        # 📂 رفع ملف
        if "file" in request.files and request.files["file"].filename:

            file = request.files["file"]
            filename = file.filename.lower()

            # ملفات نصية وبرمجية
            if filename.endswith((
                ".txt", ".py", ".js", ".html",
                ".css", ".json", ".xml",
                ".csv", ".md"
            )):

                try:
                    code = file.read().decode("utf-8")

                except:
                    code = file.read().decode(
                        "latin-1",
                        errors="ignore"
                    )

            # PDF
            elif filename.endswith(".pdf"):

                reader = PdfReader(file)

                code = "\n".join(
                    [p.extract_text() or "" for p in reader.pages]
                )

            # DOCX
            elif filename.endswith(".docx"):

                doc = Document(file)

                code = "\n".join(
                    [p.text for p in doc.paragraphs]
                )

            else:
                code = "❌ نوع الملف غير مدعوم"

        # ✍️ كود مباشر
        else:
            code = request.form.get("code_input", "")

        # التحليل
        security = security_basic(code)
        ai = ai_analyze(code)

    return render_template(
        "index.html",
        code=code,
        ai=ai,
        security=security
    )


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)