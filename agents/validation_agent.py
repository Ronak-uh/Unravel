import sqlite3""""""""""""import os

import os

import jsonValidation Agent for Unravel Automation System

import requests

Validation Agent for Unravel Automation System

class ValidationAgent:

    def __init__(self, db_path, gemini_api_key):Validates content candidates using Gemini 2.5 for quality and relevance.

        self.db_path = db_path

        self.gemini_api_key = gemini_api_key"""Validation Agent for Unravel Automation System

        self.api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"

    

    def validate_with_gemini(self, title, snippet):

        prompt = f"Analyze this tech blog idea. Title: {title}. Description: {snippet}. Return JSON with score (1-10), approved (boolean), reasoning (string), suggested_angle (string)."import sqlite3Validates content candidates using Gemini 2.5 for quality and relevance.

        

        data = {import os

            "contents": [{"parts": [{"text": prompt}]}],

            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1024}import json"""Validation Agent for Unravel Automation Systemimport json

        }

        import requests

        try:

            response = requests.post(f"{self.api_endpoint}?key={self.gemini_api_key}", 

                                   headers={'Content-Type': 'application/json'}, 

                                   json=data, timeout=30)class ValidationAgent:

            

            if response.status_code == 200:    def __init__(self, db_path, gemini_api_key):import sqlite3Validates content candidates using Gemini 2.5 for quality and relevance.

                text = response.json()['candidates'][0]['content']['parts'][0]['text']

                start, end = text.find('{'), text.rfind('}') + 1        self.db_path = db_path

                return json.loads(text[start:end])

        except Exception as e:        self.gemini_api_key = gemini_api_keyimport os

            print(f"Validation error: {e}")

                self.api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"

        return {"score": 5, "approved": True, "reasoning": "Fallback", "suggested_angle": "General tech"}

        import json"""import sqlite3

    def get_unvalidated_candidates(self, limit=10):

        conn = sqlite3.connect(self.db_path)    def validate_with_gemini(self, title, snippet):

        cursor = conn.cursor()

        cursor.execute("SELECT id, title, url, snippet FROM candidates WHERE validated = 0 LIMIT ?", (limit,))        """Validate content using Gemini 2.5 model."""import requests

        results = [{'id': r[0], 'title': r[1], 'url': r[2], 'snippet': r[3]} for r in cursor.fetchall()]

        conn.close()        prompt = f"""Analyze this content idea for a technology blog:

        return results

            

    def update_candidate_validation(self, candidate_id, score, approved, reasoning, suggested_angle):

        conn = sqlite3.connect(self.db_path)Title: {title}

        cursor = conn.cursor()

        Description: {snippet}class ValidationAgent:

        for column in [("suggested_angle", "TEXT"), ("reasoning", "TEXT")]:

            try:

                cursor.execute(f"ALTER TABLE candidates ADD COLUMN {column[0]} {column[1]}")

            except sqlite3.OperationalError:Evaluate based on relevance, quality potential, engagement, and uniqueness.    def __init__(self, db_path, gemini_api_key):import sqlite3Validates content candidates using Google Gemini AI to ensure quality and reliability.import requests

                pass

        Respond with JSON: {{"score": 1-10, "approved": true/false, "reasoning": "explanation", "suggested_angle": "angle"}}"""

        cursor.execute("UPDATE candidates SET validated = 1, score = ?, reasoning = ?, suggested_angle = ? WHERE id = ?",

                      (score, reasoning, suggested_angle, candidate_id))                self.db_path = db_path

        conn.commit()

        conn.close()        headers = {'Content-Type': 'application/json'}

        print(f"{'✅' if approved else '❌'} Candidate {candidate_id}: Score {score}/10")

            data = {        self.gemini_api_key = gemini_api_keyimport os

    def validate_candidates(self, limit=5):

        print("🔍 Starting validation phase...")            "contents": [{"parts": [{"text": prompt}]}],

        candidates = self.get_unvalidated_candidates(limit)

                    "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1024}        self.api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"

        if not candidates:

            print("📊 No candidates to validate")        }

            return 0

                    import json"""from dotenv import load_dotenv

        validated_count = 0

        for candidate in candidates:        try:

            print(f"🔍 Validating: {candidate['title'][:50]}...")

            validation = self.validate_with_gemini(candidate['title'], candidate['snippet'])            response = requests.post(f"{self.api_endpoint}?key={self.gemini_api_key}",     def validate_with_gemini(self, title, snippet):

            

            if validation:                                   headers=headers, json=data, timeout=30)

                self.update_candidate_validation(candidate['id'], validation['score'], 

                                               validation['approved'], validation['reasoning'],                     """Validate content using Gemini 2.5 model."""import requests

                                               validation['suggested_angle'])

                validated_count += 1            if response.status_code == 200:

        

        print(f"📊 Validation complete: {validated_count}/{len(candidates)} candidates processed")                text = response.json()['candidates'][0]['content']['parts'][0]['text']        prompt = f"""

        return validated_count

                    start = text.find('{')

    def get_validation_stats(self):

        conn = sqlite3.connect(self.db_path)                end = text.rfind('}') + 1        Analyze this content idea for a technology blog called "Unravel":

        cursor = conn.cursor()

                        return json.loads(text[start:end])

        cursor.execute("SELECT COUNT(*) FROM candidates WHERE validated=1")

        total_validated = cursor.fetchone()[0]            return None        

        

        cursor.execute("SELECT COUNT(*) FROM candidates WHERE validated=1 AND score >= 7")        except Exception as e:

        high_quality = cursor.fetchone()[0]

                    print(f"❌ Validation error: {str(e)}")        Title: {title}class ValidationAgent:

        cursor.execute("SELECT AVG(score) FROM candidates WHERE validated=1")

        avg_score = cursor.fetchone()[0] or 0            return {"score": 5, "approved": True, "reasoning": "Fallback approval", "suggested_angle": "General tech"}

        

        conn.close()            Description: {snippet}

        return {'total_validated': total_validated, 'high_quality': high_quality, 'average_score': round(avg_score, 2)}
    def get_unvalidated_candidates(self, limit=10):

        """Get candidates that haven't been validated yet."""            def __init__(self, db_path, gemini_api_key):import osload_dotenv()

        conn = sqlite3.connect(self.db_path)

        cursor = conn.cursor()        Evaluate based on:

        cursor.execute("SELECT id, title, url, snippet FROM candidates WHERE validated = 0 ORDER BY created_at ASC LIMIT ?", (limit,))

        candidates = cursor.fetchall()        1. Relevance to technology trends        self.db_path = db_path

        conn.close()

        return [{'id': row[0], 'title': row[1], 'url': row[2], 'snippet': row[3]} for row in candidates]        2. Content quality potential

    

    def update_candidate_validation(self, candidate_id, score, approved, reasoning, suggested_angle):        3. Audience engagement likelihood        self.gemini_api_key = gemini_api_keyimport json

        """Update candidate with validation results."""

        conn = sqlite3.connect(self.db_path)        4. Uniqueness and value

        cursor = conn.cursor()

                        self.api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"

        # Add columns if they don't exist

        for column in [("suggested_angle", "TEXT"), ("reasoning", "TEXT")]:        Respond with a JSON object containing:

            try:

                cursor.execute(f"ALTER TABLE candidates ADD COLUMN {column[0]} {column[1]}")        {{    import sqlite3GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

            except sqlite3.OperationalError:

                pass            "score": (integer 1-10),

        

        cursor.execute("UPDATE candidates SET validated = 1, score = ?, reasoning = ?, suggested_angle = ? WHERE id = ?",            "approved": (boolean),    def validate_with_gemini(self, title, snippet):

                      (score, reasoning, suggested_angle, candidate_id))

        conn.commit()            "reasoning": "Brief explanation",

        conn.close()

                    "suggested_angle": "Specific angle to cover this topic"        """Validate content using Gemini 2.5 model."""import requests

        status = "✅ APPROVED" if approved else "❌ REJECTED"

        print(f"{status} Candidate {candidate_id}: Score {score}/10")        }}

    

    def validate_candidates(self, limit=5):        """        prompt = f"""

        """Validate unvalidated candidates using Gemini 2.5."""

        print("🔍 Starting validation phase...")        

        candidates = self.get_unvalidated_candidates(limit)

                headers = {        Analyze this content idea for a technology blog called "Unravel":from dotenv import load_dotenv# Get the directory of this script and construct the path to data folder

        if not candidates:

            print("📊 No candidates to validate")            'Content-Type': 'application/json',

            return 0

                }        

        validated_count = 0

        for candidate in candidates:        

            print(f"🔍 Validating: {candidate['title'][:50]}...")

            validation = self.validate_with_gemini(candidate['title'], candidate['snippet'])        data = {        Title: {title}script_dir = os.path.dirname(os.path.abspath(__file__))

            

            if validation:            "contents": [{

                self.update_candidate_validation(candidate['id'], validation['score'], 

                                               validation['approved'], validation['reasoning'],                 "parts": [{        Description: {snippet}

                                               validation['suggested_angle'])

                validated_count += 1                    "text": prompt

            else:

                print(f"❌ Failed to validate candidate {candidate['id']}")                }]        load_dotenv()DB_PATH = os.path.join(script_dir, '..', 'data', 'sqlite.db')

        

        print(f"📊 Validation complete: {validated_count}/{len(candidates)} candidates processed")            }],

        return validated_count

                "generationConfig": {        Evaluate based on:

    def get_validation_stats(self):

        """Get validation statistics."""                "temperature": 0.3,

        conn = sqlite3.connect(self.db_path)

        cursor = conn.cursor()                "topK": 40,        1. Relevance to technology trends

        

        cursor.execute("SELECT COUNT(*) FROM candidates WHERE validated=1")                "topP": 0.95,

        total_validated = cursor.fetchone()[0]

                        "maxOutputTokens": 1024,        2. Content quality potential

        cursor.execute("SELECT COUNT(*) FROM candidates WHERE validated=1 AND score >= 7")

        high_quality = cursor.fetchone()[0]            }

        

        cursor.execute("SELECT AVG(score) FROM candidates WHERE validated=1")        }        3. Audience engagement likelihoodclass ValidationAgent:# -------------------------------

        avg_score = cursor.fetchone()[0] or 0

                

        conn.close()

        return {'total_validated': total_validated, 'high_quality': high_quality, 'average_score': round(avg_score, 2)}        try:        4. Uniqueness and value



def main():            response = requests.post(

    """Run the validation agent standalone."""

    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sqlite.db')                f"{self.api_endpoint}?key={self.gemini_api_key}",            def __init__(self, db_path):# Gemini API call wrapper

    gemini_api_key = os.getenv('GEMINI_API_KEY')

                    headers=headers,

    if not gemini_api_key:

        print("❌ GEMINI_API_KEY environment variable not set")                json=data,        Respond with a JSON object containing:

        return

                    timeout=30

    agent = ValidationAgent(db_path, gemini_api_key)

    stats = agent.get_validation_stats()            )        {{        self.db_path = db_path# -------------------------------

    print(f"📊 Validation stats: {stats}")

    agent.validate_candidates(limit=5)            

    stats = agent.get_validation_stats()

    print(f"📊 Updated validation stats: {stats}")            if response.status_code == 200:            "score": (integer 1-10),



if __name__ == "__main__":                result = response.json()

    main()
                text = result['candidates'][0]['content']['parts'][0]['text']            "approved": (boolean),        self.gemini_api_key = os.getenv("GEMINI_API_KEY")def call_gemini(prompt, model="gemini-1.5-flash"):

                

                # Extract JSON from the response            "reasoning": "Brief explanation",

                try:

                    # Find JSON content in the response            "suggested_angle": "Specific angle to cover this topic"            """

                    start = text.find('{')

                    end = text.rfind('}') + 1        }}

                    json_str = text[start:end]

                    validation_result = json.loads(json_str)        """        if not self.gemini_api_key:    Calls Gemini 1.5 Flash API with a prompt.

                    return validation_result

                except (json.JSONDecodeError, ValueError):        

                    # Fallback if JSON parsing fails

                    return {        headers = {            raise ValueError("GEMINI_API_KEY not found in environment variables")    Returns the generated text.

                        "score": 5,

                        "approved": True,            'Content-Type': 'application/json',

                        "reasoning": "Manual approval - JSON parsing failed",

                        "suggested_angle": "General technology perspective"        }        """

                    }

            else:        

                print(f"❌ Gemini API error: {response.status_code}")

                return None        data = {    def call_gemini(self, prompt, model="gemini-1.5-flash"):    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"

                

        except Exception as e:            "contents": [{

            print(f"❌ Validation error: {str(e)}")

            return None                "parts": [{        """    headers = {"Content-Type": "application/json"}

    

    def get_unvalidated_candidates(self, limit=10):                    "text": prompt

        """Get candidates that haven't been validated yet."""

        conn = sqlite3.connect(self.db_path)                }]        Calls Gemini API with a prompt.    data = {

        cursor = conn.cursor()

                    }],

        cursor.execute("""

            SELECT id, title, url, snippet             "generationConfig": {        Returns the generated text.        "contents": [{

            FROM candidates 

            WHERE validated = 0                 "temperature": 0.3,

            ORDER BY created_at ASC 

            LIMIT ?                "topK": 40,        """            "parts": [{"text": prompt}]

        """, (limit,))

                        "topP": 0.95,

        candidates = cursor.fetchall()

        conn.close()                "maxOutputTokens": 1024,        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.gemini_api_key}"        }],

        

        return [            }

            {

                'id': row[0],        }        headers = {"Content-Type": "application/json"}        "generationConfig": {

                'title': row[1],

                'url': row[2],        

                'snippet': row[3]

            }        try:        data = {            "temperature": 0.3,

            for row in candidates

        ]            response = requests.post(

    

    def update_candidate_validation(self, candidate_id, score, approved, reasoning, suggested_angle):                f"{self.api_endpoint}?key={self.gemini_api_key}",            "contents": [{            "maxOutputTokens": 500

        """Update candidate with validation results."""

        conn = sqlite3.connect(self.db_path)                headers=headers,

        cursor = conn.cursor()

                        json=data,                "parts": [{"text": prompt}]        }

        # Add suggested_angle column if it doesn't exist

        try:                timeout=30

            cursor.execute("ALTER TABLE candidates ADD COLUMN suggested_angle TEXT")

        except sqlite3.OperationalError:            )            }],    }

            pass  # Column already exists

                    

        try:

            cursor.execute("ALTER TABLE candidates ADD COLUMN reasoning TEXT")            if response.status_code == 200:            "generationConfig": {    response = requests.post(url, headers=headers, json=data)

        except sqlite3.OperationalError:

            pass  # Column already exists                result = response.json()

        

        cursor.execute("""                text = result['candidates'][0]['content']['parts'][0]['text']                "temperature": 0.3,    if response.status_code == 200:

            UPDATE candidates 

            SET validated = 1, score = ?, reasoning = ?, suggested_angle = ?                

            WHERE id = ?

        """, (score, reasoning, suggested_angle, candidate_id))                # Extract JSON from the response                "maxOutputTokens": 1000        result = response.json()

        

        conn.commit()                try:

        conn.close()

                            # Find JSON content in the response            }        if 'candidates' in result and len(result['candidates']) > 0:

        status = "✅ APPROVED" if approved else "❌ REJECTED"

        print(f"{status} Candidate {candidate_id}: Score {score}/10")                    start = text.find('{')

    

    def validate_candidates(self, limit=5):                    end = text.rfind('}') + 1        }            return result['candidates'][0]['content']['parts'][0]['text']

        """Validate unvalidated candidates using Gemini 2.5."""

        print("🔍 Starting validation phase...")                    json_str = text[start:end]

        

        candidates = self.get_unvalidated_candidates(limit)                    validation_result = json.loads(json_str)                else:

        if not candidates:

            print("📊 No candidates to validate")                    return validation_result

            return 0

                        except (json.JSONDecodeError, ValueError):        response = requests.post(url, headers=headers, json=data)            print("No content in Gemini response:", result)

        validated_count = 0

                            # Fallback if JSON parsing fails

        for candidate in candidates:

            print(f"🔍 Validating: {candidate['title'][:50]}...")                    return {        if response.status_code == 200:            return None

            

            validation = self.validate_with_gemini(                        "score": 5,

                candidate['title'],

                candidate['snippet']                        "approved": True,            result = response.json()    else:

            )

                                    "reasoning": "Manual approval - JSON parsing failed",

            if validation:

                self.update_candidate_validation(                        "suggested_angle": "General technology perspective"            if 'candidates' in result and len(result['candidates']) > 0:        print("Gemini API error:", response.text)

                    candidate['id'],

                    validation['score'],                    }

                    validation['approved'],

                    validation['reasoning'],            else:                return result['candidates'][0]['content']['parts'][0]['text']        return None

                    validation['suggested_angle']

                )                print(f"❌ Gemini API error: {response.status_code}")

                validated_count += 1

            else:                return None            else:

                print(f"❌ Failed to validate candidate {candidate['id']}")

                        

        print(f"📊 Validation complete: {validated_count}/{len(candidates)} candidates processed")

        return validated_count        except Exception as e:                print("No content in Gemini response:", result)# -------------------------------

    

    def get_validation_stats(self):            print(f"❌ Validation error: {str(e)}")

        """Get validation statistics."""

        conn = sqlite3.connect(self.db_path)            return None                return None# Build JSON validation prompt

        cursor = conn.cursor()

            

        cursor.execute("SELECT COUNT(*) FROM candidates WHERE validated=1")

        total_validated = cursor.fetchone()[0]    def get_unvalidated_candidates(self, limit=10):        else:# -------------------------------

        

        cursor.execute("SELECT COUNT(*) FROM candidates WHERE validated=1 AND score >= 7")        """Get candidates that haven't been validated yet."""

        high_quality = cursor.fetchone()[0]

                conn = sqlite3.connect(self.db_path)            print("Gemini API error:", response.text)def build_prompt(candidate):

        cursor.execute("SELECT AVG(score) FROM candidates WHERE validated=1")

        avg_score = cursor.fetchone()[0] or 0        cursor = conn.cursor()

        

        conn.close()                    return None    return f"""

        

        return {        cursor.execute("""

            'total_validated': total_validated,

            'high_quality': high_quality,            SELECT id, title, url, snippet     System: You are FactCheck-Gemini. Output JSON only.

            'average_score': round(avg_score, 2)

        }            FROM candidates 



def main():            WHERE validated = 0     def build_validation_prompt(self, candidate):

    """Run the validation agent standalone."""

    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sqlite.db')            ORDER BY created_at ASC 

    

    # Get API key from environment            LIMIT ?        """Build validation prompt for Gemini."""User: Candidate article:

    gemini_api_key = os.getenv('GEMINI_API_KEY')

    if not gemini_api_key:        """, (limit,))

        print("❌ GEMINI_API_KEY environment variable not set")

        return                return f"""title: "{candidate['title']}"

    

    agent = ValidationAgent(db_path, gemini_api_key)        candidates = cursor.fetchall()

    

    # Show current stats        conn.close()System: You are FactCheck-Gemini. Output JSON only.snippet: "{candidate['snippet']}"

    stats = agent.get_validation_stats()

    print(f"📊 Validation stats: {stats}")        

    

    # Validate candidates        return [url: "{candidate['url']}"

    agent.validate_candidates(limit=5)

                {

    # Show updated stats

    stats = agent.get_validation_stats()                'id': row[0],User: Candidate article:

    print(f"📊 Updated validation stats: {stats}")

                'title': row[1],

if __name__ == "__main__":

    main()                'url': row[2],title: "{candidate['title']}"Task: Return exactly:

                'snippet': row[3]

            }snippet: "{candidate['snippet']}"{{"accept": boolean, "score": int, "reasons": ["..."], "evidence": ["url1","url2"]}}

            for row in candidates

        ]url: "{candidate['url']}"Accept only if claims in candidate are supported by sources.

    

    def update_candidate_validation(self, candidate_id, score, approved, reasoning, suggested_angle):"""

        """Update candidate with validation results."""

        conn = sqlite3.connect(self.db_path)Task: Return exactly:

        cursor = conn.cursor()

        {{"accept": boolean, "score": int, "reasons": ["..."], "evidence": ["url1","url2"]}}# -------------------------------

        # Add suggested_angle column if it doesn't exist

        try:# Validate a single candidate

            cursor.execute("ALTER TABLE candidates ADD COLUMN suggested_angle TEXT")

        except sqlite3.OperationalError:Accept only if claims in candidate are supported by sources.# -------------------------------

            pass  # Column already exists

        Score 1-100 based on:def validate_candidate(candidate):

        try:

            cursor.execute("ALTER TABLE candidates ADD COLUMN reasoning TEXT")- Factual accuracy (40%)    prompt = build_prompt(candidate)

        except sqlite3.OperationalError:

            pass  # Column already exists- Source credibility (30%)     resp = call_gemini(prompt)

        

        cursor.execute("""- Content relevance (20%)    if resp is None:

            UPDATE candidates 

            SET validated = 1, score = ?, reasoning = ?, suggested_angle = ?- Writing quality (10%)        return None

            WHERE id = ?

        """, (score, reasoning, suggested_angle, candidate_id))

        

        conn.commit()Provide specific reasons for accept/reject decision.    try:

        conn.close()

        Include evidence URLs that support or contradict claims.        # Remove markdown code blocks if present

        status = "✅ APPROVED" if approved else "❌ REJECTED"

        print(f"{status} Candidate {candidate_id}: Score {score}/10")"""        if resp.strip().startswith("```json"):

    

    def validate_candidates(self, limit=5):                resp = resp.strip()[7:]

        """Validate unvalidated candidates using Gemini 2.5."""

        print("🔍 Starting validation phase...")    def validate_candidate(self, candidate):        if resp.strip().endswith("```"):

        

        candidates = self.get_unvalidated_candidates(limit)        """Validate a single candidate using Gemini."""            resp = resp.strip()[:-3]

        if not candidates:

            print("📊 No candidates to validate")        prompt = self.build_validation_prompt(candidate)        

            return 0

                resp = self.call_gemini(prompt)        data = json.loads(resp.strip())

        validated_count = 0

                        return data

        for candidate in candidates:

            print(f"🔍 Validating: {candidate['title'][:50]}...")        if resp is None:    except json.JSONDecodeError:

            

            validation = self.validate_with_gemini(            return None        print("Failed to parse Gemini response:", resp)

                candidate['title'],

                candidate['snippet']                return None

            )

                    try:

            if validation:

                self.update_candidate_validation(            # Remove markdown code blocks if present# -------------------------------

                    candidate['id'],

                    validation['score'],            if resp.strip().startswith("```json"):# Run validation on all unvalidated candidates

                    validation['approved'],

                    validation['reasoning'],                resp = resp.strip()[7:]# -------------------------------

                    validation['suggested_angle']

                )            if resp.strip().endswith("```"):def run_validation():

                validated_count += 1

            else:                resp = resp.strip()[:-3]    conn = sqlite3.connect(DB_PATH)

                print(f"❌ Failed to validate candidate {candidate['id']}")

                        c = conn.cursor()

        print(f"📊 Validation complete: {validated_count}/{len(candidates)} candidates processed")

        return validated_count            data = json.loads(resp.strip())    c.execute("SELECT id, title, url, snippet FROM candidates WHERE validated=0")

    

    def get_validation_stats(self):            return data    candidates = c.fetchall()

        """Get validation statistics."""

        conn = sqlite3.connect(self.db_path)        except json.JSONDecodeError:

        cursor = conn.cursor()

                    print("Failed to parse Gemini response:", resp)    for cand in candidates:

        cursor.execute("SELECT COUNT(*) FROM candidates WHERE validated=1")

        total_validated = cursor.fetchone()[0]            return None        candidate = {"id": cand[0], "title": cand[1], "url": cand[2], "snippet": cand[3]}

        

        cursor.execute("SELECT COUNT(*) FROM candidates WHERE validated=1 AND score >= 7")            result = validate_candidate(candidate)

        high_quality = cursor.fetchone()[0]

            def get_unvalidated_candidates(self):        if result:

        cursor.execute("SELECT AVG(score) FROM candidates WHERE validated=1")

        avg_score = cursor.fetchone()[0] or 0        """Get all unvalidated candidates from database."""            c.execute("""

        

        conn.close()        conn = sqlite3.connect(self.db_path)            UPDATE candidates

        

        return {        cursor = conn.cursor()            SET validated=1, score=?, published=0

            'total_validated': total_validated,

            'high_quality': high_quality,                    WHERE id=?

            'average_score': round(avg_score, 2)

        }        cursor.execute("SELECT id, title, url, snippet FROM candidates WHERE validated=0")            """, (result.get('score', 0), candidate['id']))



def main():        candidates = cursor.fetchall()            conn.commit()

    """Run the validation agent standalone."""

    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sqlite.db')                    print(f"Validated: {candidate['title']} → Accept={result.get('accept')}, Score={result.get('score')}")

    

    # Get API key from environment        conn.close()

    gemini_api_key = os.getenv('GEMINI_API_KEY')

    if not gemini_api_key:            conn.close()

        print("❌ GEMINI_API_KEY environment variable not set")

        return        return [

    

    agent = ValidationAgent(db_path, gemini_api_key)            {"id": cand[0], "title": cand[1], "url": cand[2], "snippet": cand[3]}# -------------------------------

    

    # Show current stats            for cand in candidates# Run standalone

    stats = agent.get_validation_stats()

    print(f"📊 Validation stats: {stats}")        ]# -------------------------------

    

    # Validate candidates    if __name__ == "__main__":

    agent.validate_candidates(limit=5)

        def update_candidate_validation(self, candidate_id, validation_result):    run_validation()

    # Show updated stats        """Update candidate in database with validation results."""

    stats = agent.get_validation_stats()        conn = sqlite3.connect(self.db_path)

    print(f"📊 Updated validation stats: {stats}")        cursor = conn.cursor()

        

if __name__ == "__main__":        score = validation_result.get('score', 0)

    main()        
        cursor.execute("""
        UPDATE candidates
        SET validated=1, score=?, published=0
        WHERE id=?
        """, (score, candidate_id))
        
        conn.commit()
        conn.close()
    
    def run_validation(self):
        """Run validation on all unvalidated candidates."""
        print("🔍 Running validation agent...")
        
        candidates = self.get_unvalidated_candidates()
        
        if not candidates:
            print("📭 No candidates to validate.")
            return 0
        
        validated_count = 0
        
        for candidate in candidates:
            print(f"🔍 Validating: {candidate['title'][:50]}...")
            
            result = self.validate_candidate(candidate)
            
            if result:
                self.update_candidate_validation(candidate['id'], result)
                validated_count += 1
                
                accept = result.get('accept', False)
                score = result.get('score', 0)
                
                print(f"✓ Validated: {candidate['title'][:50]}... → Accept={accept}, Score={score}")
            else:
                print(f"❌ Failed to validate: {candidate['title'][:50]}...")
        
        print(f"📊 Validation complete: {validated_count} candidates validated")
        return validated_count
    
    def get_validation_stats(self):
        """Get validation statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM candidates WHERE validated=0")
        unvalidated = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM candidates WHERE validated=1")
        validated = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(score) FROM candidates WHERE validated=1")
        avg_score = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'unvalidated': unvalidated,
            'validated': validated,
            'average_score': round(avg_score, 2)
        }

def main():
    """Run the validation agent standalone."""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sqlite.db')
    agent = ValidationAgent(db_path)
    
    # Show current stats
    stats = agent.get_validation_stats()
    print(f"📊 Validation stats: {stats}")
    
    # Run validation
    validated = agent.run_validation()
    
    # Show updated stats
    stats = agent.get_validation_stats()
    print(f"📊 Updated stats: {stats}")

if __name__ == "__main__":
    main()