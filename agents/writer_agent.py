import os
import sqlite3
from dotenv import load_dotenv
import requests

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sqlite.db")

# -------------------------------
# Gemini call
# -------------------------------
def call_gemini(prompt, model="gemini-1.5-pro"):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.5,
            "maxOutputTokens": 1000
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if 'candidates' in result and len(result['candidates']) > 0:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            print("No candidates in Gemini response:", result)
            return None
    else:
        print("Gemini error:", response.text)
        return None

# -------------------------------
# Build prompt
# -------------------------------
def build_prompt(candidate):
    return f"""
System: You are BlogWriter-Gemini. Output ONLY Markdown with YAML front matter.

User: Write a ~800 word blog post.
Title: {candidate['title']}
Tone: casual
Keywords: AI, blogging
Evidence summary: score={candidate['score']}, snippet="{candidate['snippet']}"
Requirements:
- Output Markdown only
- YAML front matter with title, meta_description, tags
- Headings, short examples, conclusion, sources section
"""

# -------------------------------
# Generate Markdown
# -------------------------------
def write_post(candidate):
    md = call_gemini(build_prompt(candidate))
    return md

# -------------------------------
# Generate for all validated but unpublished candidates (limit 4)
# -------------------------------
def run_writer(limit=4):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Check if we have the enhanced schema with content and category columns
    c.execute("PRAGMA table_info(candidates)")
    columns = [column[1] for column in c.fetchall()]
    has_content_column = 'content' in columns
    has_image_columns = 'featured_image_url' in columns
    has_category_column = 'category' in columns
    
    if has_content_column and has_image_columns and has_category_column:
        c.execute("""SELECT id, title, snippet, score, content, featured_image_url, 
                     featured_image_alt, image_keywords, category 
                     FROM candidates WHERE validated=1 AND published=0 LIMIT ?""", (limit,))
        candidates = c.fetchall()
        
        for cand in candidates:
            candidate = {
                "id": cand[0], "title": cand[1], "snippet": cand[2], "score": cand[3], 
                "content": cand[4], "featured_image_url": cand[5], 
                "featured_image_alt": cand[6], "image_keywords": cand[7], "category": cand[8]
            }
            
            # Get associated images from post_images table
            c.execute("""SELECT image_url, alt_text, caption, image_type, position 
                        FROM post_images WHERE candidate_id = ? ORDER BY position""", (candidate['id'],))
            images = c.fetchall()
            candidate['images'] = [
                {"url": img[0], "alt_text": img[1], "caption": img[2], "type": img[3], "position": img[4]}
                for img in images
            ]
            
            md = write_post(candidate)
            if md:
                # store Markdown temporarily in DB or file
                data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
                with open(os.path.join(data_dir, f"post_{candidate['id']}.md"), "w", encoding="utf-8") as f:
                    f.write(md)
                print(f"Written post: {candidate['title']}")
    else:
        # Fallback to old query for backward compatibility
        c.execute("SELECT id, title, snippet, score FROM candidates WHERE validated=1 AND published=0 LIMIT ?", (limit,))
        candidates = c.fetchall()
        
        for cand in candidates:
            candidate = {"id": cand[0], "title": cand[1], "snippet": cand[2], "score": cand[3]}
            md = write_post(candidate)
            if md:
                # store Markdown temporarily in DB or file
                data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
                with open(os.path.join(data_dir, f"post_{candidate['id']}.md"), "w", encoding="utf-8") as f:
                    f.write(md)
                print(f"Written post: {candidate['title']}")

    conn.close()

# -------------------------------
if __name__ == "__main__":
    run_writer(limit=4)