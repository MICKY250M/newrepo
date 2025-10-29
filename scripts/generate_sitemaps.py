import os
import glob
import json # تم إضافة مكتبة JSON
from slugify import slugify
from datetime import datetime

# الثوابت
OUTPUT_DIR = 'posts'
SITEMAP_INDEX_FILE = 'sitemap_index.xml'
SITEMAP_BASE_NAME = 'sitemap'
POSTS_PER_SITEMAP = 1000  

def generate_sitemaps():
    """
    يجد جميع ملفات Markdown وينشئ خرائط الموقع وملف فهرس JSON.
    """
    print("Starting sitemap and JSON index generation...")
    
    post_files = sorted(glob.glob(os.path.join(OUTPUT_DIR, '*.md')))
    if not post_files:
        print("No articles found in the posts directory. Skipping generation.")
        return

    sitemap_files = []
    
    for i, start_index in enumerate(range(0, len(post_files), POSTS_PER_SITEMAP)):
        sitemap_posts = post_files[start_index:start_index + POSTS_PER_SITEMAP]
        sitemap_name = f"{SITEMAP_BASE_NAME}_{i+1}.xml"
        sitemap_files.append(sitemap_name)
        
        sitemap_content = create_sitemap_content(sitemap_posts, sitemap_name)
        
        with open(sitemap_name, 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        
        print(f"Generated {sitemap_name} with {len(sitemap_posts)} URLs.")

    create_sitemap_index(sitemap_files)
    generate_json_index(post_files) # استدعاء الدالة الجديدة

    print("Generation complete.")


def create_sitemap_content(post_paths: list, sitemap_name: str) -> str:
    """تنشئ محتوى XML لخريطة موقع فردية."""
    # يجب استبدال هذا برابط مدونتك الحقيقي
    BASE_URL = "https://MICKY250M.github.io/newrepo" 
    
    now = datetime.now().isoformat(timespec='seconds') + "+00:00"
    
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""
    
    for path in post_paths:
        file_name = os.path.basename(path).replace('.md', '')
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
    BASE_URL = "https://MICKY250M.github.io/newrepo"
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


def generate_json_index(post_paths: list):
    """تنشئ ملف JSON يحتوي على قائمة المقالات وعناوينها."""
    index_data = []
    
    for path in post_paths:
        file_name = os.path.basename(path)
        # استخراج العنوان الجميل من اسم الملف
        title_raw = file_name.replace(/(\d{4}-|-)|\.md/g, ' ').trim()
        title = ' '.join(title_raw.split()).title() # تنسيق العنوان (حرف كبير لكل كلمة)

        index_data.append({
            "fileName": file_name,
            "title": title
        })

    with open('index.json', 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=4)

    print("Generated index.json successfully.")


if __name__ == '__main__':
    generate_sitemaps()
