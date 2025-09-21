import os, requests, sqlite3
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("GOOGLE_CSE_ID")

def search_google(query, num=3):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": API_KEY, "cx": CSE_ID, "q": query, "num": num}
    r = requests.get(url, params=params, timeout=10).json()
    items = r.get('items', [])
    results = []
    for it in items:
        results.append({
            "title": it.get("title"),
            "link": it.get("link"),
            "snippet": it.get("snippet")
        })
    return results

def find_topics(seed_terms, max_per_term=3):
    candidates = []
    for term in seed_terms:
        results = search_google(term, num=max_per_term)
        for r in results:
            candidates.append(r)
    # Save to SQLite and return new candidates
    return candidates