import os
import json
import re
from datetime import datetime

POSTS_DIR = "posts"
INDEX_FILE = "index.json"

def get_title_from_filename(filename):
    """
    Converts a clean filename (e.g., the-future-of-daos.md) back into a readable title.
    """
    if not filename.endswith(".md"):
        return filename  # Return as is if not a markdown file
        
    # Remove the .md extension
    title = filename[:-3] 
    
    # Replace hyphens with spaces
    title = title.replace('-', ' ')
    
    # Capitalize the first letter of each word
    title = title.title()
    
    return title

def update_index():
    """
    Scans the posts directory, builds a new index.json file, and adds metadata.
    """
    if not os.path.exists(POSTS_DIR):
        print(f"Directory '{POSTS_DIR}' not found. Index file will be empty.")
        articles_data = []
    else:
        # Get all files ending with .md from the posts directory
        all_files = os.listdir(POSTS_DIR)
        markdown_files = sorted([f for f in all_files if f.endswith('.md')])

        articles_data = []
        for filename in markdown_files:
            # Create a clean title for the sidebar display
            readable_title = get_title_from_filename(filename)
            
            # Get file modification timestamp (optional but good practice)
            # This requires reading the file stats, which is fast.
            filepath = os.path.join(POSTS_DIR, filename)
            
            # Note: GitHub Actions usually sets the modification time to the commit time.
            timestamp = os.path.getmtime(filepath)
            last_mod = datetime.fromtimestamp(timestamp).isoformat()
            
            article_entry = {
                "title": readable_title,
                "fileName": filename,
                "lastModified": last_mod
            }
            articles_data.append(article_entry)

        print(f"Found {len(articles_data)} article(s) in {POSTS_DIR}.")

    # Add the current timestamp for the index itself (optional metadata)
    index_metadata = {
        "updated_at": datetime.now().isoformat(),
        "articles": articles_data
    }
    
    # Save the full data structure to index.json
    try:
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            # Use indent for readability in the repository
            json.dump(index_metadata, f, ensure_ascii=False, indent=4)
        print(f"SUCCESS: Index file '{INDEX_FILE}' updated.")
    except Exception as e:
        print(f"Error saving index file: {e}")

if __name__ == "__main__":
    update_index()
