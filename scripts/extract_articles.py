import os
import pathlib
from docx import Document
from slugify import slugify

# الثوابت
# اسم ملف الموسوعة (يجب أن يكون موجوداً في جذر المستودع)
DOCX_FILE = 'encyclopedia.docx'
# مسار المجلد الذي سيتم حفظ المقالات فيه
OUTPUT_DIR = 'posts'

def is_title(paragraph_text: str) -> bool:
    """
    تتحقق ما إذا كانت الفقرة هي عنوان رئيسي جديد للمقال.
    نعتمد على تنسيق Markdown (#) كما حدده المستخدم.
    """
    # يجب أن يبدأ بـ # مسافة
    return paragraph_text.startswith('# ')

def clean_content(text: str) -> str:
    """
    تنظيف محتوى الفقرة من رموز Markdown للعناوين الفرعية
    والحروف الزائدة مثل المسافات والسطور الفارغة في البداية والنهاية.
    """
    # إزالة رموز العناوين الفرعية (#, ##, ###) التي قد تظهر داخل جسم المقال
    text = text.lstrip('#').strip()
    
    # استبدال السطور الفارغة المتكررة بسطر فارغ واحد
    text = os.linesep.join([s for s in text.splitlines() if s.strip()])
    
    return text

def extract_articles(doc_path: str):
    """
    يقرأ ملف Word (docx)، يستخرج المقالات بناءً على التنسيق المحدد،
    ويحفظ كل مقال كملف Markdown منفصل.
    """
    try:
        document = Document(doc_path)
    except Exception as e:
        print(f"Error loading document {doc_path}: {e}")
        return

    # إنشاء مجلد posts إذا لم يكن موجوداً
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # حل مشكلة عدم ظهور المجلد: إنشاء ملف .gitkeep
    pathlib.Path(os.path.join(OUTPUT_DIR, '.gitkeep')).touch()
    
    current_article = []
    article_title = ""
    article_count = 0

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        
        # تخطي الفقرات الفارغة تمامًا
        if not text:
            continue

        if is_title(text):
            # حفظ المقال السابق قبل البدء بالجديد
            if current_article:
                save_article(article_title, current_article, article_count)
            
            # بدء مقال جديد
            article_count += 1
            lines = text.split('\n')
            
            # البحث عن العنوان الرئيسي (يبدأ بـ #)
            main_title_line = next((line for line in lines if line.strip().startswith('# ')), None)
            
            if main_title_line:
                article_title = main_title_line.lstrip('# ').strip()
            else:
                article_title = "Untitled Article"

            current_article = []
            
            # إضافة العنوان إلى بداية المقال في ملف Markdown
            current_article.append(f"# {article_title}\n")
            
            # إضافة باقي المحتوى في نفس الفقرة إن وجد (مثل العنوان الفرعي)
            remaining_content = [clean_content(line) for line in lines if not line.strip().startswith('# ')]
            if remaining_content:
                current_article.extend([f"{line}\n" for line in remaining_content if line])
            
        elif current_article:
            # إضافة المحتوى إلى المقال الحالي
            cleaned_text = clean_content(text)
            if cleaned_text:
                current_article.append(cleaned_text + "\n")

    # حفظ المقال الأخير
    if current_article:
        save_article(article_title, current_article, article_count)

    print(f"Extraction complete. Total articles saved: {article_count}")


def save_article(title: str, content: list, count: int):
    """
    يحفظ محتوى المقال في ملف Markdown.
    """
    # *** التعديل لحل مشكلة TypeError: تمت إزالة to_lower=True ***
    file_slug = slugify(title, max_length=50) 
    file_name = f"{count:04d}-{file_slug}.md"
    file_path = os.path.join(OUTPUT_DIR, file_name)

    article_content = "\n".join(content).strip()

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(article_content)
        print(f"Saved: {file_path}")
    except Exception as e:
        print(f"Error saving file {file_path}: {e}")

if __name__ == '__main__':
    if not os.path.exists(DOCX_FILE):
        print(f"Error: The document '{DOCX_FILE}' was not found in the repository root.")
    else:
        extract_articles(DOCX_FILE)
