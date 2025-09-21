import os
import jwt
import datetime
import requests
from dotenv import load_dotenv
import sqlite3
import markdown


load_dotenv()

GHOST_ADMIN_API_KEY = os.getenv("GHOST_ADMIN_API_KEY")  # format: id:secret
GHOST_URL = os.getenv("GHOST_URL", "http://localhost:2368")
DB_PATH = "../data/sqlite.db"

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
# Publish a single post
# -------------------------------
def publish_post(title, md_content):
    token = ghost_jwt()
    html_content = markdown.markdown(md_content)
    headers = {"Authorization": f"Ghost {token}", "Content-Type": "application/json"}
    post_data = {"posts":[{"title": title, "html": html_content, "status": "published"}]}
    r = requests.post(API_URL, headers=headers, json=post_data)
    if r.status_code == 201 or r.status_code == 200:
        return True
    else:
        print("Publish failed:", r.text)
        return False

# -------------------------------
# Publish all Markdown posts
# -------------------------------
def run_publisher():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title FROM candidates WHERE validated=1 AND published=0")
    posts = c.fetchall()

    for post in posts:
        post_id, title = post
        md_file = f"../data/post_{post_id}.md"
        if os.path.exists(md_file):
            with open(md_file, "r", encoding="utf-8") as f:
                md_content = f.read()
            if publish_post(title, md_content):
                c.execute("UPDATE candidates SET published=1 WHERE id=?", (post_id,))
                conn.commit()
                print(f"Published: {title}")

    conn.close()

# -------------------------------
if __name__ == "__main__":
    run_publisher()