#!/usr/bin/env python3
"""
Unravel - Automated Content Generation & Publishing Pipeline
Complete automation system in a single file.

This script:
1. Validates candidates using Gemini API
2. Writes blog posts using AI
3. Publishes to Ghost CMS (4 posts per run)

Usage: python automation.py
For cron: python /path/to/automation.py
"""

import os
import json
import sqlite3
import requests
import markdown
import jwt
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GHOST_ADMIN_API_KEY = os.getenv("GHOST_ADMIN_API_KEY")
GHOST_URL = os.getenv("GHOST_URL", "http://localhost:2368")

# Get the directory of this script and construct paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, 'data', 'sqlite.db')
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')

# API URLs
GHOST_API_URL = f"{GHOST_URL}/ghost/api/admin/posts/"

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# ================================
# GEMINI API FUNCTIONS
# ================================

def call_gemini(prompt, model="gemini-1.5-flash"):
    """
    Calls Gemini API with a prompt.
    Returns the generated text.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 1000
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if 'candidates' in result and len(result['candidates']) > 0:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            print("No content in Gemini response:", result)
            return None
    else:
        print("Gemini API error:", response.text)
        return None

# ================================
# VALIDATION FUNCTIONS
# ================================

def build_validation_prompt(candidate):
    """Build validation prompt for Gemini."""
    return f"""
System: You are FactCheck-Gemini. Output JSON only.

User: Candidate article:
title: "{candidate['title']}"
snippet: "{candidate['snippet']}"
url: "{candidate['url']}"

Task: Return exactly:
{{"accept": boolean, "score": int, "reasons": ["..."], "evidence": ["url1","url2"]}}
Accept only if claims in candidate are supported by sources.
"""

def validate_candidate(candidate):
    """Validate a single candidate using Gemini."""
    prompt = build_validation_prompt(candidate)
    resp = call_gemini(prompt)
    if resp is None:
        return None

    try:
        # Remove markdown code blocks if present
        if resp.strip().startswith("```json"):
            resp = resp.strip()[7:]
        if resp.strip().endswith("```"):
            resp = resp.strip()[:-3]
        
        data = json.loads(resp.strip())
        return data
    except json.JSONDecodeError:
        print("Failed to parse Gemini response:", resp)
        return None

def run_validation():
    """Run validation on all unvalidated candidates."""
    print("🔍 Running validation agent...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, url, snippet FROM candidates WHERE validated=0")
    candidates = c.fetchall()

    validated_count = 0
    for cand in candidates:
        candidate = {"id": cand[0], "title": cand[1], "url": cand[2], "snippet": cand[3]}
        result = validate_candidate(candidate)
        if result:
            c.execute("""
            UPDATE candidates
            SET validated=1, score=?, published=0
            WHERE id=?
            """, (result.get('score', 0), candidate['id']))
            conn.commit()
            validated_count += 1
            print(f"✓ Validated: {candidate['title'][:50]}... → Accept={result.get('accept')}, Score={result.get('score')}")

    conn.close()
    print(f"📊 Validation complete: {validated_count} candidates validated")

# ================================
# WRITING FUNCTIONS
# ================================

def build_writing_prompt(candidate):
    """Build writing prompt for Gemini."""
    return f"""
System: You are BlogWriter-Gemini. Output ONLY Markdown with YAML front matter.

User: Write a ~800 word blog post.
Title: {candidate['title']}
Tone: casual
Keywords: AI, blogging, technology
Evidence summary: score={candidate['score']}, snippet="{candidate['snippet']}"

Requirements:
- Start with YAML front matter between --- delimiters (not code blocks)
- Include title, meta_description, tags in YAML
- Follow with markdown content including an image at the top
- Use headings, examples, conclusion
- Add a sources section at the end

Example format:
---
title: "Your Title Here"
meta_description: "Brief description"
tags: ["AI", "blogging", "technology"]
---

![Featured Image](https://via.placeholder.com/800x400/0066cc/ffffff?text=Blog+Post+Image)

# Your Title Here

Your content here...

## Conclusion

...

## Sources

...

IMPORTANT: Include an image right after the YAML frontmatter using markdown format:
![Alt Text](https://via.placeholder.com/800x400/0066cc/ffffff?text=Tech+News)
"""

def write_post(candidate):
    """Generate markdown content for a candidate."""
    md = call_gemini(build_writing_prompt(candidate))
    return md

def run_writer():
    """Generate content for all validated but unpublished candidates."""
    print("✍️ Running writer agent...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, snippet, score FROM candidates WHERE validated=1 AND published=0")
    candidates = c.fetchall()

    written_count = 0
    for cand in candidates:
        candidate = {"id": cand[0], "title": cand[1], "snippet": cand[2], "score": cand[3]}
        md = write_post(candidate)
        if md:
            post_file = os.path.join(DATA_DIR, f"post_{candidate['id']}.md")
            with open(post_file, "w", encoding="utf-8") as f:
                f.write(md)
            written_count += 1
            print(f"✓ Written: {candidate['title'][:50]}...")

    conn.close()
    print(f"📝 Writing complete: {written_count} posts written")

# ================================
# GHOST PUBLISHING FUNCTIONS
# ================================

def ghost_jwt():
    """Generate JWT for Ghost Admin API."""
    id, secret = GHOST_ADMIN_API_KEY.split(':')
    iat = int(datetime.datetime.now().timestamp())
    payload = {"iat": iat, "exp": iat + 5*60, "aud": "/admin/"}
    token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers={"kid": id})
    return token

def publish_post(title, md_content):
    """Publish a single post to Ghost CMS."""
    token = ghost_jwt()
    
    # Handle YAML frontmatter (no longer extracting featured_image)
    if md_content.startswith('---'):
        parts = md_content.split('---', 2)
        if len(parts) >= 3:
            md_body = parts[2].strip()
        else:
            md_body = md_content
    else:
        md_body = md_content
    
    # Convert markdown to HTML (this will convert the ![image] to <img> tags)
    html_content = markdown.markdown(
        md_body, 
        extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite']
    )
    
    # Create mobiledoc format for Ghost
    mobiledoc = {
        "version": "0.3.1",
        "atoms": [],
        "cards": [
            ["html", {"html": html_content}]
        ],
        "markups": [],
        "sections": [
            [10, 0]
        ]
    }
    
    headers = {"Authorization": f"Ghost {token}", "Content-Type": "application/json"}
    post_data = {
        "posts": [{
            "title": title,
            "mobiledoc": json.dumps(mobiledoc),
            "status": "published",
            "visibility": "public"
        }]
    }
    
    r = requests.post(GHOST_API_URL, headers=headers, json=post_data)
    if r.status_code == 201 or r.status_code == 200:
        return True
    else:
        print(f"❌ Publish failed for '{title}': {r.text}")
        return False

def run_publisher():
    """Publish posts to Ghost CMS (limit to 4 per run)."""
    print("🚀 Running publisher agent...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Limit to 4 posts per run
    c.execute("SELECT id, title FROM candidates WHERE validated=1 AND published=0 LIMIT 4")
    posts = c.fetchall()

    if not posts:
        print("📭 No posts to publish.")
        conn.close()
        return

    print(f"📤 Publishing {len(posts)} posts...")
    
    published_count = 0
    for post in posts:
        post_id, title = post
        md_file = os.path.join(DATA_DIR, f"post_{post_id}.md")
        
        if os.path.exists(md_file):
            with open(md_file, "r", encoding="utf-8") as f:
                md_content = f.read()
            
            if publish_post(title, md_content):
                c.execute("UPDATE candidates SET published=1 WHERE id=?", (post_id,))
                conn.commit()
                published_count += 1
                print(f"✅ Published: {title[:50]}...")
            else:
                print(f"❌ Failed: {title[:50]}...")
        else:
            print(f"❌ No markdown file: post_{post_id}.md")

    conn.close()
    print(f"🎉 Publishing complete: {published_count}/{len(posts)} posts published")

# ================================
# DATABASE STATS
# ================================

def show_stats():
    """Show current database statistics."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get total counts
    c.execute("SELECT COUNT(*) FROM candidates")
    total = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM candidates WHERE validated=0")
    unvalidated = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM candidates WHERE validated=1 AND published=0")
    ready_to_publish = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM candidates WHERE validated=1 AND published=1")
    published = c.fetchone()[0]
    
    conn.close()
    
    print("\n📊 DATABASE STATISTICS:")
    print(f"   Total candidates: {total}")
    print(f"   Unvalidated: {unvalidated}")
    print(f"   Ready to publish: {ready_to_publish}")
    print(f"   Published: {published}")

# ================================
# MAIN AUTOMATION PIPELINE
# ================================

def main():
    """Run the complete automation pipeline."""
    print("🤖 UNRAVEL AUTOMATION PIPELINE STARTED")
    print("=" * 50)
    
    try:
        # Check environment variables
        if not GEMINI_API_KEY:
            print("❌ Error: GEMINI_API_KEY not found in environment")
            return
        
        if not GHOST_ADMIN_API_KEY:
            print("❌ Error: GHOST_ADMIN_API_KEY not found in environment")
            return
        
        print(f"🌐 Ghost URL: {GHOST_URL}")
        print(f"🗄️ Database: {DB_PATH}")
        
        # Show initial stats
        show_stats()
        
        # Run pipeline steps
        print("\n" + "=" * 50)
        
        # Step 1: Validation
        run_validation()
        
        print("\n" + "-" * 30)
        
        # Step 2: Writing
        run_writer()
        
        print("\n" + "-" * 30)
        
        # Step 3: Publishing (limited to 4 posts)
        run_publisher()
        
        # Show final stats
        print("\n" + "=" * 50)
        show_stats()
        
        print("\n✨ PIPELINE COMPLETE! Check your Ghost CMS for new posts.")
        
    except Exception as e:
        print(f"❌ Pipeline error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()