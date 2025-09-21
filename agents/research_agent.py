import os
import requests
import sqlite3
import time
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from readability import Document

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("GOOGLE_CSE_KEY")
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sqlite.db")

def extract_article_content(url):
    """Extract the main content from an article URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Use readability to extract main content
        doc = Document(response.text)  # Use .text instead of .content
        title = doc.title()
        content = doc.summary()
        
        # Clean up the content using BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            element.decompose()
        
        # Extract text content
        text_content = soup.get_text(separator='\n', strip=True)
        
        # Clean up extra whitespace
        lines = [line.strip() for line in text_content.split('\n') if line.strip()]
        clean_content = '\n'.join(lines)
        
        # Limit content length to prevent database bloat
        if len(clean_content) > 5000:
            clean_content = clean_content[:5000] + "..."
        
        return {
            'title': title or "No title",
            'content': clean_content,
            'success': True
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Network error extracting content from {url}: {e}")
        return {'title': '', 'content': '', 'success': False}
    except Exception as e:
        print(f"Error extracting content from {url}: {e}")
        return {'title': '', 'content': '', 'success': False}

def search_images(query, num=3):
    """Search for images related to the query"""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY, 
        "cx": CSE_ID, 
        "q": query, 
        "num": num,
        "searchType": "image",
        "safe": "active",
        "imgSize": "large",
        "imgType": "photo"
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        items = data.get('items', [])
        
        images = []
        for item in items:
            # Get image metadata
            image_data = {
                "url": item.get("link"),
                "title": item.get("title", ""),
                "alt_text": item.get("snippet", ""),
                "width": item.get("image", {}).get("width", 0),
                "height": item.get("image", {}).get("height", 0),
                "thumbnail": item.get("image", {}).get("thumbnailLink", ""),
                "context_url": item.get("image", {}).get("contextLink", "")
            }
            
            # Filter out very small images or non-web formats
            if (image_data["width"] >= 400 and 
                image_data["height"] >= 300 and
                any(ext in image_data["url"].lower() for ext in ['.jpg', '.jpeg', '.png', '.webp'])):
                images.append(image_data)
        
        return images
    except requests.exceptions.RequestException as e:
        print(f"Error searching images for '{query}': {e}")
        return []
    except Exception as e:
        print(f"Unexpected error in image search: {e}")
        return []

def categorize_content(title, snippet, search_term, content=None):
    """Categorize content based on title, snippet, and search term for Ghost CMS tags"""
    # Combine all text for analysis
    text = f"{title} {snippet} {search_term}".lower()
    if content:
        text += f" {content[:500]}".lower()  # First 500 chars of content
    
    # Category mapping based on keywords
    categories = {
        'India': ['india', 'indian', 'mumbai', 'delhi', 'bangalore', 'bollywood', 'rupee', 'modi', 'bjp', 'congress', 'hindi'],
        'World': ['global', 'international', 'world', 'europe', 'asia', 'america', 'africa', 'united nations', 'nato', 'g7', 'g20', 'china', 'usa', 'uk'],
        'Stocks': ['stock', 'shares', 'market', 'trading', 'investment', 'portfolio', 'nasdaq', 'dow jones', 's&p', 'equity', 'dividend', 'nse', 'bse'],
        'Technology': ['tech', 'ai', 'artificial intelligence', 'software', 'hardware', 'startup', 'innovation', 'digital', 'cyber'],
        'Finance': ['finance', 'banking', 'cryptocurrency', 'bitcoin', 'economic', 'inflation', 'gdp', 'recession', 'fintech'],
        'Health': ['health', 'medical', 'healthcare', 'hospital', 'medicine', 'vaccine', 'disease', 'wellness', 'pharma'],
        'Business': ['business', 'company', 'corporate', 'industry', 'merger', 'acquisition', 'revenue', 'profit', 'enterprise'],
        'Sports': ['sports', 'football', 'cricket', 'basketball', 'olympics', 'fifa', 'athlete', 'tournament', 'ipl'],
        'Entertainment': ['movie', 'film', 'celebrity', 'music', 'entertainment', 'netflix', 'streaming', 'gaming', 'bollywood'],
        'Politics': ['politics', 'election', 'government', 'policy', 'law', 'supreme court', 'parliament', 'senate', 'minister']
    }
    
    # Score each category
    category_scores = {}
    for category, keywords in categories.items():
        score = sum(1 for keyword in keywords if keyword in text)
        if score > 0:
            category_scores[category] = score
    
    # Return the category with highest score, or 'General' if no match
    if category_scores:
        return max(category_scores.items(), key=lambda x: x[1])[0]
    else:
        return 'General'

def search_google(query, num=2):
    url = "https://www.googleapis.com/customsearch/v1"
    # Add date filter for more recent content
    params = {
        "key": API_KEY, 
        "cx": CSE_ID, 
        "q": query, 
        "num": num,
        "sort": "date",  # Sort by date to get recent content
        "dateRestrict": "d7"  # Get content from last 7 days
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        items = data.get('items', [])
        results = []
        
        for it in items:
            article_data = {
                "title": it.get("title"),
                "link": it.get("link"),
                "snippet": it.get("snippet")
            }
            
            # Extract full content for each article
            print(f"  Extracting content from: {article_data['link']}")
            content_data = extract_article_content(article_data['link'])
            
            if content_data['success']:
                article_data['content'] = content_data['content']
                article_data['extracted_title'] = content_data['title']
            else:
                article_data['content'] = article_data['snippet']  # Fallback to snippet
                
            results.append(article_data)
            
            # Be nice to servers - small delay between requests
            time.sleep(1)
            
        return results
    except requests.exceptions.RequestException as e:
        print(f"Error searching Google for '{query}': {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def save_candidates_to_db(candidates):
    """Save candidate articles and their images to the database"""
    if not candidates:
        print("No candidates to save")
        return
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # First, let's check if content and category columns exist, if not add them
    try:
        c.execute("ALTER TABLE candidates ADD COLUMN content TEXT")
        conn.commit()
        print("Added content column to database")
    except sqlite3.OperationalError:
        # Column already exists
        pass
    
    try:
        c.execute("ALTER TABLE candidates ADD COLUMN category TEXT DEFAULT 'General'")
        conn.commit()
        print("Added category column to database")
    except sqlite3.OperationalError:
        # Column already exists
        pass
    
    saved_count = 0
    for candidate in candidates:
        try:
            # Check if URL already exists to avoid duplicates
            c.execute("SELECT id FROM candidates WHERE url = ?", (candidate['link'],))
            existing = c.fetchone()
            
            if existing is None:
                # Categorize the content
                category = categorize_content(
                    candidate.get('title', ''),
                    candidate.get('snippet', ''),
                    candidate.get('search_term', ''),
                    candidate.get('content', '')
                )
                
                # Insert the candidate
                c.execute("""
                INSERT INTO candidates (title, url, snippet, content, featured_image_url, 
                                      featured_image_alt, image_keywords, category, validated, published)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0)
                """, (candidate['title'], candidate['link'], candidate['snippet'], 
                     candidate.get('content', candidate['snippet']),
                     candidate.get('featured_image_url'),
                     candidate.get('featured_image_alt'),
                     candidate.get('image_keywords'),
                     category))
                
                candidate_id = c.lastrowid
                
                # Save associated images
                if 'images' in candidate:
                    for i, img in enumerate(candidate['images']):
                        image_type = 'featured' if i == 0 else 'content'
                        c.execute("""
                        INSERT INTO post_images (candidate_id, image_url, alt_text, caption, 
                                               image_type, position)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """, (candidate_id, img['url'], img['alt_text'], img['title'], 
                             image_type, i))
                
                saved_count += 1
                
        except sqlite3.Error as e:
            print(f"Database error saving candidate '{candidate.get('title', 'Unknown')}': {e}")
    
    conn.commit()
    conn.close()
    print(f"Saved {saved_count} new candidates to database")

def find_topics(seed_terms, max_per_term=2):
    candidates = []
    for term in seed_terms:
        print(f"Searching for: {term}")
        results = search_google(term, num=max_per_term)
        
        for r in results:
            # Add search term for categorization
            r['search_term'] = term
            
            # Search for images related to this article
            print(f"  Finding images for: {r['title'][:50]}...")
            
            # Create search query for images based on title and snippet
            image_query = f"{r['title']} {term}"
            images = search_images(image_query, num=2)
            
            if images:
                r['images'] = images
                r['featured_image_url'] = images[0]['url']
                r['featured_image_alt'] = images[0]['alt_text']
                r['image_keywords'] = image_query
                print(f"    Found {len(images)} images")
            else:
                print(f"    No suitable images found")
                
            candidates.append(r)
    
    # Save to SQLite
    save_candidates_to_db(candidates)
    return candidates

def run_research(seed_terms=None):
    """Main function to run research with default or provided terms"""
    if seed_terms is None:
        # Diverse topics covering multiple categories
        seed_terms = [
            # Technology & Innovation
            "breakthrough technology 2025", "startup funding news", "cybersecurity trends",
            # Health & Science
            "medical breakthrough", "climate change solutions", "space exploration news",
            # Finance & Business
            "market trends", "cryptocurrency news", "economic forecast 2025",
            # Entertainment & Culture
            "movie industry news", "gaming industry updates", "social media trends",
            # Sports & Lifestyle
            "sports technology", "fitness trends", "travel destinations 2025",
            # Politics & Society
            "policy changes 2025", "education reform", "sustainable living",
            # General Interest
            "productivity tips", "career advancement", "mental health awareness"
        ]
    
    print("=== Starting Research Agent ===")
    print(f"API Key present: {'Yes' if API_KEY else 'No'}")
    print(f"CSE ID present: {'Yes' if CSE_ID else 'No'}")
    
    if not API_KEY or not CSE_ID:
        print("Missing required environment variables: GOOGLE_API_KEY or GOOGLE_CSE_KEY")
        return
    
    candidates = find_topics(seed_terms)
    print(f"Research complete. Found {len(candidates)} total candidates.")
    return candidates

# Run standalone
if __name__ == "__main__":
    run_research()
