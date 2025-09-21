#!/usr/bin/env python3


import os
import json
import sqlite3
import requests
import markdown
import jwt
import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import feedparser
import time
import random

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
# DATABASE SETUP
# ================================

def setup_database():
    """Create and initialize the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create candidates table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        url TEXT,
        snippet TEXT,
        validated INTEGER DEFAULT 0,
        score INTEGER DEFAULT 0,
        published INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

# ================================
# GEMINI API FUNCTIONS
# ================================

def call_gemini(prompt, model="gemini-2.0-flash-exp"):
    """
    Calls Gemini 2.5 API with a prompt.
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
# RESEARCH FUNCTIONS
# ================================

def get_trending_topics():
    """Get trending topics by scraping multiple tech news sources."""
    trending_topics = []
    
    # Tech news sources to scrape
    sources = [
        {
            "name": "TechCrunch RSS",
            "url": "https://techcrunch.com/feed/",
            "type": "rss"
        },
        {
            "name": "Hacker News",
            "url": "https://hnrss.org/frontpage",
            "type": "rss"
        },
        {
            "name": "The Verge RSS",
            "url": "https://www.theverge.com/rss/index.xml",
            "type": "rss"
        },
        {
            "name": "Ars Technica RSS",
            "url": "https://feeds.arstechnica.com/arstechnica/index",
            "type": "rss"
        }
    ]
    
    print("🌐 Scraping trending tech topics from multiple sources...")
    
    for source in sources:
        try:
            print(f"📡 Fetching from {source['name']}...")
            
            if source['type'] == 'rss':
                # Parse RSS feeds
                feed = feedparser.parse(source['url'])
                
                for entry in feed.entries[:3]:  # Get top 3 from each source
                    # Clean up the title and summary
                    title = entry.title.strip()
                    summary = getattr(entry, 'summary', getattr(entry, 'description', ''))
                    
                    # Remove HTML tags from summary
                    if summary:
                        soup = BeautifulSoup(summary, 'html.parser')
                        summary = soup.get_text().strip()[:200] + "..."
                    
                    topic = {
                        "title": title,
                        "url": getattr(entry, 'link', source['url']),
                        "snippet": summary or f"Latest trending topic from {source['name']}: {title}"
                    }
                    
                    trending_topics.append(topic)
                    print(f"  ✓ Found: {title[:60]}...")
            
            # Add a small delay to be respectful to servers
            time.sleep(1)
            
        except Exception as e:
            print(f"  ⚠️ Error fetching from {source['name']}: {str(e)}")
            continue
    
    # If we couldn't fetch any real topics, fall back to curated ones
    if not trending_topics:
        print("🔄 Using fallback curated topics...")
        trending_topics = [
            {
                "title": "AI-Powered Content Creation Revolution",
                "url": "https://techcrunch.com/ai-content-creation",
                "snippet": "Explore how artificial intelligence is transforming content creation for bloggers and marketers."
            },
            {
                "title": "Future of Remote Work Technology",
                "url": "https://theverge.com/remote-work-tech",
                "snippet": "Discover the latest technologies reshaping how teams collaborate remotely."
            },
            {
                "title": "Sustainable Tech Innovations 2025",
                "url": "https://arstechnica.com/sustainable-tech",
                "snippet": "Breakthrough technologies helping create a more sustainable digital future."
            },
            {
                "title": "Quantum Computing Breakthroughs",
                "url": "https://hackernews.com/quantum-computing",
                "snippet": "Latest advances in quantum computing and their real-world applications."
            },
            {
                "title": "Cybersecurity in Cloud Era",
                "url": "https://techcrunch.com/cloud-security",
                "snippet": "Essential cybersecurity practices for modern cloud-based businesses."
            }
        ]
    
    # Shuffle and limit to avoid always getting the same order
    random.shuffle(trending_topics)
    selected_topics = trending_topics[:8]  # Limit to 8 topics
    
    print(f"📊 Found {len(selected_topics)} trending topics to process")
    return selected_topics

def run_research():
    """Add new content candidates to the database by scraping trending topics."""
    print("🔍 Running research phase...")
    
    setup_database()
    
    # Fetch trending topics from multiple sources
    topics = get_trending_topics()
    added_count = 0
    duplicate_count = 0
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for topic in topics:
        # Check if topic already exists (by title or similar URL)
        cursor.execute("SELECT COUNT(*) FROM candidates WHERE title=? OR url=?", 
                      (topic['title'], topic['url']))
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO candidates (title, url, snippet) VALUES (?, ?, ?)",
                (topic['title'], topic['url'], topic['snippet'])
            )
            added_count += 1
            print(f"  ✅ Added: {topic['title'][:60]}...")
        else:
            duplicate_count += 1
            print(f"  🔄 Duplicate: {topic['title'][:60]}...")
    
    conn.commit()
    conn.close()
    
    print(f"📊 Research complete: {added_count} new candidates added, {duplicate_count} duplicates skipped")
    return added_count

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
Tone: casual, engaging, informative
Keywords: AI, blogging, technology, innovation
Evidence summary: score={candidate['score']}, snippet="{candidate['snippet']}"

Requirements:
- Start with YAML front matter between --- delimiters (not code blocks)
- Include title, meta_description, tags in YAML
- Follow with markdown content including an image at the top
- Use headings, examples, practical tips, conclusion
- Add a sources section at the end
- Make it engaging and actionable

Example format:
---
title: "Your Title Here"
meta_description: "Brief description under 160 characters"
tags: ["AI", "blogging", "technology"]
---

![Featured Image](https://via.placeholder.com/800x400/0066cc/ffffff?text=Blog+Post+Image)

# Your Title Here

Engaging introduction paragraph that hooks the reader...

## Main Content Section

Your detailed content here with practical examples...

## Another Section

More valuable content...

## Conclusion

Wrap up with key takeaways and actionable insights...

## Sources

- Reference sources and additional reading

IMPORTANT: Include an image right after the YAML frontmatter using markdown format:
![Tech News](https://via.placeholder.com/800x400/0066cc/ffffff?text=Tech+News)

Make the content valuable, actionable, and engaging for readers interested in technology and innovation.
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
    
    # Handle YAML frontmatter
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

def show_stats():
    """Show current database statistics."""
    import sqlite3
    
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
    
    print("\\n📊 DATABASE STATISTICS:")
    print(f"   Total candidates: {total}")
    print(f"   Unvalidated: {unvalidated}")
    print(f"   Ready to publish: {ready_to_publish}")
    print(f"   Published: {published}")

def main():
    """Run the complete automation pipeline using modular agents."""
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
        
        print("\\n" + "=" * 50)
        
        # Step 1: Research (add new candidates)
        run_research()
        
        print("\\n" + "-" * 30)
        
        # Step 2: Validation
        run_validation()
        
        print("\\n" + "-" * 30)
        
        # Step 3: Writing (with embedded images)
        run_writer()
        
        print("\\n" + "-" * 30)
        
        # Step 4: Publishing (limited to 4 posts with images)
        run_publisher()
        
        # Show final stats
        print("\\n" + "=" * 50)
        show_stats()
        
        print("\\n✨ PIPELINE COMPLETE! Check your Ghost CMS for new posts.")
        
    except Exception as e:
        print(f"❌ Pipeline error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()