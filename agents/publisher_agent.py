import os
import jwt
import datetime
import requests
from dotenv import load_dotenv
import sqlite3
import markdown
import json
import re
from urllib.parse import urlparse


load_dotenv()

GHOST_ADMIN_API_KEY = os.getenv("GHOST_ADMIN_API_KEY")  # format: id:secret
GHOST_URL = os.getenv("GHOST_URL", "http://localhost:2368")
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sqlite.db")

API_URL = f"{GHOST_URL}/ghost/api/admin/posts/"

# -------------------------------
# Generate JWT for Ghost
# -------------------------------
def ghost_jwt():
    id, secret = GHOST_ADMIN_API_KEY.split(':')
    iat = int(datetime.datetime.now().timestamp())
    payload = {"iat": iat, "exp": iat + 5*60, "aud": "/admin/"}
    token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers={"kid": id})
    return token

# -------------------------------
# Upload image to Ghost CMS
# -------------------------------
def upload_image_to_ghost(image_url, alt_text=""):
    """Upload an image from URL to Ghost CMS and return the Ghost image URL"""
    try:
        # Download the image first
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        img_response = requests.get(image_url, headers=headers, timeout=15)
        img_response.raise_for_status()
        
        # Get file extension
        parsed_url = urlparse(image_url)
        filename = os.path.basename(parsed_url.path)
        if not filename or '.' not in filename:
            filename = "image.jpg"
        
        # Upload to Ghost
        token = ghost_jwt()
        upload_url = f"{GHOST_URL}/ghost/api/admin/images/upload/"
        upload_headers = {"Authorization": f"Ghost {token}"}
        
        files = {'file': (filename, img_response.content, img_response.headers.get('content-type', 'image/jpeg'))}
        
        upload_response = requests.post(upload_url, headers=upload_headers, files=files)
        upload_response.raise_for_status()
        
        result = upload_response.json()
        ghost_url = result['images'][0]['url']
        print(f"✓ Uploaded image: {filename}")
        return ghost_url
        
    except Exception as e:
        print(f"Error uploading image {image_url}: {e}")
        return None

# -------------------------------
# Process markdown content with images
# -------------------------------
def process_content_with_images(md_content, candidate_id):
    """Replace image placeholders with uploaded Ghost images"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get images for this candidate
    c.execute("""SELECT image_url, alt_text, caption, image_type, uploaded_to_ghost, ghost_image_url 
                 FROM post_images WHERE candidate_id = ? ORDER BY position""", (candidate_id,))
    images = c.fetchall()
    
    content_images = []
    featured_image_url = None
    
    for img in images:
        image_url, alt_text, caption, image_type, uploaded, ghost_url = img
        
        # Upload image if not already uploaded
        if not uploaded or not ghost_url:
            ghost_url = upload_image_to_ghost(image_url, alt_text)
            if ghost_url:
                # Update database with Ghost URL
                c.execute("""UPDATE post_images SET uploaded_to_ghost=1, ghost_image_url=? 
                           WHERE candidate_id=? AND image_url=?""", 
                         (ghost_url, candidate_id, image_url))
                conn.commit()
        
        if ghost_url:
            if image_type == 'featured':
                featured_image_url = ghost_url
            else:
                content_images.append({
                    'url': ghost_url,
                    'alt': alt_text or caption or 'Related image',
                    'caption': caption
                })
    
    conn.close()
    
    # Replace IMAGE_PLACEHOLDER with actual images in content
    if content_images:
        placeholder_pattern = r'!\[([^\]]*)\]\(IMAGE_PLACEHOLDER\)'
        
        def replace_placeholder(match):
            if content_images:
                img = content_images.pop(0)
                return f"![{img['alt']}]({img['url']})"
            return match.group(0)
        
        md_content = re.sub(placeholder_pattern, replace_placeholder, md_content)
    
    return md_content, featured_image_url

# -------------------------------
# Get category tags for Ghost CMS
# -------------------------------
def get_ghost_tags(candidate_id):
    """Get category-based tags for Ghost CMS"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get category from database
    c.execute("SELECT category FROM candidates WHERE id = ?", (candidate_id,))
    result = c.fetchone()
    conn.close()
    
    if result and result[0]:
        category = result[0]
        # Return the category as a tag
        return [{"name": category}]
    else:
        return [{"name": "General"}]

# -------------------------------
# Publish a single post
# -------------------------------
def publish_post(title, md_content, candidate_id=None):
    token = ghost_jwt()
    
    # Process images if candidate_id is provided
    featured_image_url = None
    tags = []
    if candidate_id:
        md_content, featured_image_url = process_content_with_images(md_content, candidate_id)
        tags = get_ghost_tags(candidate_id)
    
    # Extract content without YAML front matter for HTML conversion
    lines = md_content.split('\n')
    content_start = 0
    in_yaml_block = False
    
    # Skip YAML front matter if present (handles both ```yaml...``` and ---...--- formats)
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('```yaml') or stripped == '---':
            in_yaml_block = True
            continue
        elif (stripped == '```' or stripped == '---') and in_yaml_block:
            content_start = i + 1
            break
    
    # Get the main content without YAML front matter
    main_content = '\n'.join(lines[content_start:]).strip()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(main_content, extensions=['extra', 'codehilite'])
    
    # Create mobiledoc format for better compatibility
    mobiledoc = {
        "version": "0.3.1",
        "markups": [],
        "atoms": [],
        "cards": [["html", {"html": html_content}]],
        "sections": [[10, 0]]
    }
    
    headers = {"Authorization": f"Ghost {token}", "Content-Type": "application/json"}
    post_data = {
        "posts": [{
            "title": title, 
            "mobiledoc": json.dumps(mobiledoc),
            "status": "published",
            "tags": tags  # Add category tags
        }]
    }
    
    # Add featured image if available
    if featured_image_url:
        post_data["posts"][0]["feature_image"] = featured_image_url
    
    r = requests.post(API_URL, headers=headers, json=post_data)
    if r.status_code == 201 or r.status_code == 200:
        return True
    else:
        print("Publish failed:", r.text)
        return False

# -------------------------------
# Publish Markdown posts (limit 4)
# -------------------------------
def run_publisher(limit=4):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title FROM candidates WHERE validated=1 AND published=0 LIMIT ?", (limit,))
    posts = c.fetchall()

    for post in posts:
        post_id, title = post
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        md_file = os.path.join(data_dir, f"post_{post_id}.md")
        if os.path.exists(md_file):
            with open(md_file, "r", encoding="utf-8") as f:
                md_content = f.read()
            if publish_post(title, md_content, candidate_id=post_id):
                c.execute("UPDATE candidates SET published=1 WHERE id=?", (post_id,))
                conn.commit()
                print(f"Published: {title}")
            else:
                print(f"Failed to publish: {title}")

    conn.close()

# -------------------------------
if __name__ == "__main__":
    run_publisher(limit=4)