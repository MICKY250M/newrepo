import os
import requests
import json
import re
from datetime import datetime

# --- Configuration ---
# Your Hugging Face API Token must be set as an environment variable (HF_TOKEN)
HF_TOKEN = os.environ.get("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
POSTS_DIR = "posts"
TITLES_FILE = "titles.txt"
LOG_FILE = "log.txt"

def clean_filename(title):
    """Converts a title into a clean, SEO-friendly filename."""
    # Convert title to lowercase
    title = title.lower()
    # Replace non-alphanumeric characters with hyphens
    title = re.sub(r'[^a-z0-9]+', '-', title).strip('-')
    # Limit consecutive hyphens
    title = re.sub(r'-+', '-', title)
    return title

def generate_article(title):
    """Generates an article using the Hugging Face Inference API."""
    if not HF_TOKEN:
        print("Error: HF_TOKEN environment variable is not set. Cannot connect to API.")
        return None

    # Prompt structure for the Mistral model
    prompt = (
        f"You are an expert article writer. Write a full, well-structured, SEO-friendly article "
        f"about the following topic. The output must be pure markdown content, "
        f"starting with a Level 1 header (# Title) followed by an introduction, "
        f"multiple Level 2 and 3 subheadings (## and ###) for structure, and a concluding paragraph. "
        f"Do not include any external links, YAML front matter, or code blocks in this draft.\n\n"
        f"Topic: {title}"
    )

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 1500,  # Max output length
            "temperature": 0.8,
            "return_full_text": False  # Only return the generated part
        },
        "options": {
            "wait_for_model": True  # Wait if the model is loading
        }
    }

    try:
        print(f"-> Sending request to Hugging Face API for: {title}")
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        data = response.json()
        
        # Extract the generated text from the response structure
        if data and isinstance(data, list) and 'generated_text' in data[0]:
            article_content = data[0]['generated_text'].strip()
            return article_content
        
        print(f"Error: API response format was unexpected: {data}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Hugging Face API: {e}")
        return None

def process_titles():
    """Reads the first title, generates the article, and updates the files."""
    if not os.path.exists(TITLES_FILE):
        print(f"Error: Titles file '{TITLES_FILE}' not found. Exiting.")
        return

    # 1. Read titles queue
    with open(TITLES_FILE, 'r', encoding='utf-8') as f:
        titles = [line.strip() for line in f if line.strip()]

    if not titles:
        print("Titles queue is empty. No articles to generate.")
        return

    current_title = titles.pop(0)  # Get the first title and remove it from the list
    print(f"Starting generation for title: {current_title}")

    # 2. Generate content
    markdown_content = generate_article(current_title)

    if markdown_content:
        # 3. Save the article file
        filename = clean_filename(current_title) + ".md"
        filepath = os.path.join(POSTS_DIR, filename)

        if not os.path.exists(POSTS_DIR):
            os.makedirs(POSTS_DIR)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"SUCCESS: Article saved to {filepath}")

        # 4. Update the log file
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - GENERATED: {current_title} -> {filename}\n"
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        print(f"Log updated: {LOG_FILE}")

        # 5. Rewrite the titles file (removes the processed title)
        with open(TITLES_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(titles) + ('\n' if titles else ''))
        
        print(f"Titles file updated. Titles remaining: {len(titles)}")

    else:
        print(f"FAILED to generate content for: {current_title}. Title remains in queue.")

if __name__ == "__main__":
    process_titles()
