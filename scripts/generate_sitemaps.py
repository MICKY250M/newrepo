import os
import glob
from slugify import slugify
from datetime import datetime

# الثوابت
OUTPUT_DIR = 'posts'
SITEMAP_INDEX_FILE = 'sitemap_index.xml'
SITEMAP_BASE_NAME = 'sitemap'
POSTS_PER_SITEMAP = 1000  # الحد الأقصى المسموح به في خريطة موقع واحدة

def generate_sitemaps():
    """
    يجد جميع ملفات Markdown في مجلد posts وينشئ خرائط الموقع (Sitemaps)
    وملف فهرس خرائط الموقع (Sitemap Index).
    """
    print("Starting sitemap generation...")
    
    # العثور على جميع ملفات المقالات
    # يحدد المسار إلى ملفات Markdown داخل مجلد posts
    post_files = sorted(glob.glob(os.path.join(OUTPUT_DIR, '*.md')))
    if not post_files:
        print("No articles found in the posts directory. Skipping sitemap generation.")
        return

    sitemap_files = []
    
    # تقسيم المقالات إلى مجموعات
    for i, start_index in enumerate(range(0, len(post_files), POSTS_PER_SITEMAP)):
        sitemap_posts = post_files[start_index:start_index + POSTS_PER_SITEMAP]
        sitemap_name = f"{SITEMAP_BASE_NAME}_{i+1}.xml"
        sitemap_files.append(sitemap_name)
        
        # توليد محتوى خريطة الموقع الفردية
        sitemap_content = create_sitemap_content(sitemap_posts, sitemap_name)
        
        # حفظ الملف في جذر المستودع
        with open(sitemap_name, 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        
        print(f"Generated {sitemap_name} with {len(sitemap_posts)} URLs.")

    # توليد ملف فهرس خرائط الموقع
    create_sitemap_index(sitemap_files)
    
    print("Sitemap generation complete.")


def create_sitemap_content(post_paths: list, sitemap_name: str) -> str:
    """تنشئ محتوى XML لخريطة موقع فردية."""
    # **تعديل: يجب استبدال هذا برابط مدونتك الحقيقي**
    BASE_URL = "https://MICKY250M.github.io/your-repo-name" 
    
    # تنسيق الوقت ليكون متوافقًا مع XML
    now = datetime.now().isoformat(timespec='seconds') + "+00:00"
    
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""
    
    for path in post_paths:
        # استخراج اسم الملف بدون المسار والامتداد (مثال: 0001-productivity)
        file_name = os.path.basename(path).replace('.md', '')
        
        # افتراض أن رابط المقال سيكون: BASE_URL/posts/file_name/
        url = f"{BASE_URL}/posts/{file_name}/" 
        
        xml_content += f"""  <url>
    <loc>{url}</loc>
    <lastmod>{now}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
"""
        
    xml_content += "</urlset>"
    return xml_content


def create_sitemap_index(sitemap_files: list):
    """تنشئ ملف فهرس خرائط الموقع (Sitemap Index)."""
    # **تعديل: يجب استبدال هذا برابط مدونتك الحقيقي**
    BASE_URL = "https://MICKY250M.github.io/your-repo-name"
    now = datetime.now().isoformat(timespec='seconds') + "+00:00"

    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

    for sitemap in sitemap_files:
        url = f"{BASE_URL}/{sitemap}"
        xml_content += f"""  <sitemap>
    <loc>{url}</loc>
    <lastmod>{now}</lastmod>
  </sitemap>
"""

    xml_content += "</sitemapindex>"

    with open(SITEMAP_INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"Generated {SITEMAP_INDEX_FILE}.")

if __name__ == '__main__':
    generate_sitemaps()
