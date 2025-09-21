import os
import sqlite3
from dotenv import load_dotenv
import requests

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DB_PATH = "../data/sqlite.db"

# -------------------------------
# Gemini call
# -------------------------------
def call_gemini(prompt, model="gemini-2.5-pro"):
    url = f"https://generativeai.googleapis.com/v1beta/models/{model}/generate"
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}", "Content-Type": "application/json"}
    data = {"prompt": prompt, "temperature": 0.5, "maxOutputTokens": 1000}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['candidates'][0]['output']
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
# Generate for all validated but unpublished candidates
# -------------------------------
def run_writer():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, snippet, score FROM candidates WHERE validated=1 AND published=0")
    candidates = c.fetchall()

    for cand in candidates:
        candidate = {"id": cand[0], "title": cand[1], "snippet": cand[2], "score": cand[3]}
        md = write_post(candidate)
        if md:
            # store Markdown temporarily in DB or file
            with open(f"../data/post_{candidate['id']}.md", "w", encoding="utf-8") as f:
                f.write(md)
            print(f"Written post: {candidate['title']}")

    conn.close()

# -------------------------------
if __name__ == "__main__":
    run_writer()