import os
import json
import sqlite3
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DB_PATH = "../data/sqlite.db"

# -------------------------------
# Gemini API call wrapper
# -------------------------------
def call_gemini(prompt, model="gemini-2.5-pro"):
    """
    Calls Gemini 2.5 Pro API with a prompt.
    Returns the generated text.
    """
    url = "https://generativeai.googleapis.com/v1beta/models/{}/generate".format(model)
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}", "Content-Type": "application/json"}
    data = {
        "prompt": prompt,
        "temperature": 0.3,
        "maxOutputTokens": 500
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['candidates'][0]['output']
    else:
        print("Gemini API error:", response.text)
        return None

# -------------------------------
# Build JSON validation prompt
# -------------------------------
def build_prompt(candidate):
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

# -------------------------------
# Validate a single candidate
# -------------------------------
def validate_candidate(candidate):
    prompt = build_prompt(candidate)
    resp = call_gemini(prompt)
    if resp is None:
        return None

    try:
        data = json.loads(resp)
        return data
    except json.JSONDecodeError:
        print("Failed to parse Gemini response:", resp)
        return None

# -------------------------------
# Run validation on all unvalidated candidates
# -------------------------------
def run_validation():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, url, snippet FROM candidates WHERE validated=0")
    candidates = c.fetchall()

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
            print(f"Validated: {candidate['title']} → Accept={result.get('accept')}, Score={result.get('score')}")

    conn.close()

# -------------------------------
# Run standalone
# -------------------------------
if __name__ == "__main__":
    run_validation()