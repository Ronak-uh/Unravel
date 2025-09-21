import sqlite3"""""""""import os

import os

import jsonWriter Agent for Unravel Automation System

import requests

Writer Agent for Unravel Automation System

class WriterAgent:

    def __init__(self, db_path, gemini_api_key):Generates high-quality blog content using Gemini 2.5 with embedded images.

        self.db_path = db_path

        self.gemini_api_key = gemini_api_key"""Writer Agent for Unravel Automation Systemimport sqlite3

        self.api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"

    

    def generate_content_with_gemini(self, title, snippet, suggested_angle):

        prompt = f"""Write a blog post for "Unravel" tech blog:import sqlite3Generates high-quality blog content using Gemini 2.5 with embedded images.

Title: {title}

Description: {snippet}import os

Angle: {suggested_angle}

import json"""from dotenv import load_dotenv

Return JSON with: title, excerpt, content (markdown), tags array, meta_description, image_prompt"""

        import requests

        data = {

            "contents": [{"parts": [{"text": prompt}]}],import base64

            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}

        }from datetime import datetime

        

        try:import sqlite3Generates engaging blog post content using Google Gemini AI.import requests

            response = requests.post(f"{self.api_endpoint}?key={self.gemini_api_key}", 

                                   headers={'Content-Type': 'application/json'}, class WriterAgent:

                                   json=data, timeout=60)

                def __init__(self, db_path, gemini_api_key):import os

            if response.status_code == 200:

                text = response.json()['candidates'][0]['content']['parts'][0]['text']        self.db_path = db_path

                start, end = text.find('{'), text.rfind('}') + 1

                return json.loads(text[start:end])        self.gemini_api_key = gemini_api_keyimport jsonCreates markdown files with YAML frontmatter and embedded images.

        except Exception as e:

            print(f"Content generation error: {e}")        self.api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"

        

        return None        self.image_api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:generateImage"import requests

    

    def get_validated_candidates(self, limit=5):    

        conn = sqlite3.connect(self.db_path)

        cursor = conn.cursor()    def generate_image(self, prompt):import base64"""load_dotenv()

        

        try:        """Generate image using Gemini's image generation (placeholder - may not be available)."""

            cursor.execute("ALTER TABLE candidates ADD COLUMN content_generated INTEGER DEFAULT 0")

        except sqlite3.OperationalError:        # For now, return None as image generation might not be availablefrom datetime import datetime

            pass

                # Could be implemented when the API becomes available

        cursor.execute("""

            SELECT id, title, snippet, suggested_angle, score        return None

            FROM candidates 

            WHERE validated = 1 AND content_generated = 0 AND score >= 6    

            ORDER BY score DESC LIMIT ?

        """, (limit,))    def generate_content_with_gemini(self, title, snippet, suggested_angle):class WriterAgent:

        

        results = [{'id': r[0], 'title': r[1], 'snippet': r[2],         """Generate blog content using Gemini 2.5."""

                   'suggested_angle': r[3] or 'General tech', 'score': r[4]} 

                  for r in cursor.fetchall()]        prompt = f"""Write a comprehensive blog post for "Unravel" technology blog:    def __init__(self, db_path, gemini_api_key):import osGEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

        conn.close()

        return results

    

    def save_generated_content(self, candidate_id, content_data):Title: {title}        self.db_path = db_path

        conn = sqlite3.connect(self.db_path)

        cursor = conn.cursor()Description: {snippet}

        

        columns = [("generated_title", "TEXT"), ("excerpt", "TEXT"), ("content", "TEXT"),Angle: {suggested_angle}        self.gemini_api_key = gemini_api_keyimport sqlite3

                  ("tags", "TEXT"), ("meta_description", "TEXT"), ("content_generated", "INTEGER DEFAULT 0")]

        

        for column_name, column_type in columns:

            try:Requirements:        self.api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"

                cursor.execute(f"ALTER TABLE candidates ADD COLUMN {column_name} {column_type}")

            except sqlite3.OperationalError:- 800-1200 words

                pass

        - Engaging introduction        self.image_api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:generateImage"import requests# Get the directory of this script and construct the path to data folder

        cursor.execute("""

            UPDATE candidates - Well-structured sections

            SET generated_title = ?, excerpt = ?, content = ?, tags = ?, 

                meta_description = ?, content_generated = 1- Practical insights    

            WHERE id = ?

        """, (content_data['title'], content_data['excerpt'], content_data['content'],- Professional but accessible tone

              ','.join(content_data['tags']), content_data['meta_description'], candidate_id))

        - Markdown formatting    def generate_image(self, prompt):from dotenv import load_dotenvscript_dir = os.path.dirname(os.path.abspath(__file__))

        conn.commit()

        conn.close()

        

        # Save to fileReturn JSON: {{"title": "post title", "excerpt": "brief preview", "content": "markdown content", "tags": ["tag1", "tag2"], "meta_description": "SEO description", "image_prompt": "image description"}}"""        """Generate image using Gemini's image generation."""

        data_dir = os.path.dirname(self.db_path)

        filepath = os.path.join(data_dir, f"post_{candidate_id}.md")        

        

        with open(filepath, 'w', encoding='utf-8') as f:        headers = {'Content-Type': 'application/json'}        headers = {DB_PATH = os.path.join(script_dir, '..', 'data', 'sqlite.db')

            f.write(f"# {content_data['title']}\n\n")

            f.write(f"**Tags:** {', '.join(content_data['tags'])}\n\n")        data = {

            f.write("---\n\n")

            f.write(content_data['content'])            "contents": [{"parts": [{"text": prompt}]}],            'Content-Type': 'application/json',

        

        print(f"💾 Content saved: post_{candidate_id}.md")            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}

    

    def write_content(self, limit=3):        }        }load_dotenv()

        print("✍️ Starting content generation phase...")

        candidates = self.get_validated_candidates(limit)        

        

        if not candidates:        try:        

            print("📊 No candidates ready for content generation")

            return 0            response = requests.post(f"{self.api_endpoint}?key={self.gemini_api_key}", 

        

        generated_count = 0                                   headers=headers, json=data, timeout=60)        data = {# -------------------------------

        for candidate in candidates:

            print(f"✍️ Writing: {candidate['title'][:50]}...")            

            

            content = self.generate_content_with_gemini(candidate['title'], candidate['snippet'], candidate['suggested_angle'])            if response.status_code == 200:            "prompt": f"Professional blog header image: {prompt}. Clean, modern, tech-focused design.",

            

            if content:                text = response.json()['candidates'][0]['content']['parts'][0]['text']

                self.save_generated_content(candidate['id'], content)

                generated_count += 1                start = text.find('{')            "config": {class WriterAgent:# Gemini call

                print(f"✅ Content generated for candidate {candidate['id']}")

            else:                end = text.rfind('}') + 1

                print(f"❌ Failed to generate content for candidate {candidate['id']}")

                        return json.loads(text[start:end])                "aspectRatio": "16:9",

        print(f"📊 Content generation complete: {generated_count}/{len(candidates)} posts written")

        return generated_count            return None

    

    def get_writing_stats(self):        except Exception as e:                "quality": "standard"    def __init__(self, db_path, data_dir):# -------------------------------

        conn = sqlite3.connect(self.db_path)

        cursor = conn.cursor()            print(f"❌ Content generation error: {str(e)}")

        

        try:            return None            }

            cursor.execute("SELECT COUNT(*) FROM candidates WHERE content_generated=1")

            total_written = cursor.fetchone()[0]    

            

            cursor.execute("SELECT COUNT(*) FROM candidates WHERE validated=1 AND content_generated=0")    def get_validated_candidates(self, limit=5):        }        self.db_path = db_pathdef call_gemini(prompt, model="gemini-1.5-flash"):

            ready_to_write = cursor.fetchone()[0]

        except sqlite3.OperationalError:        """Get validated candidates that haven't been written yet."""

            total_written = ready_to_write = 0

                conn = sqlite3.connect(self.db_path)        

        conn.close()

        return {'total_written': total_written, 'with_images': 0, 'ready_to_write': ready_to_write}        cursor = conn.cursor()

                try:        self.data_dir = data_dir    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"

        # Add content_generated column if it doesn't exist

        try:            response = requests.post(

            cursor.execute("ALTER TABLE candidates ADD COLUMN content_generated INTEGER DEFAULT 0")

        except sqlite3.OperationalError:                f"{self.image_api_endpoint}?key={self.gemini_api_key}",        self.gemini_api_key = os.getenv("GEMINI_API_KEY")    headers = {"Content-Type": "application/json"}

            pass

                        headers=headers,

        cursor.execute("""

            SELECT id, title, snippet, suggested_angle, score                json=data,            data = {

            FROM candidates 

            WHERE validated = 1 AND content_generated = 0 AND score >= 6                timeout=60

            ORDER BY score DESC, created_at ASC

            LIMIT ?            )        if not self.gemini_api_key:        "contents": [{

        """, (limit,))

                    

        candidates = cursor.fetchall()

        conn.close()            if response.status_code == 200:            raise ValueError("GEMINI_API_KEY not found in environment variables")            "parts": [{"text": prompt}]

        

        return [{'id': row[0], 'title': row[1], 'snippet': row[2],                 result = response.json()

                'suggested_angle': row[3] or 'General technology perspective', 'score': row[4]} 

                for row in candidates]                if 'generatedImages' in result and result['generatedImages']:                }],

    

    def save_generated_content(self, candidate_id, content_data, image_data=None):                    # Return base64 image data

        """Save generated content to database and file."""

        conn = sqlite3.connect(self.db_path)                    return result['generatedImages'][0]['bytesBase64Encoded']        # Ensure data directory exists        "generationConfig": {

        cursor = conn.cursor()

                    else:

        # Add content columns if they don't exist

        columns = [("generated_title", "TEXT"), ("excerpt", "TEXT"), ("content", "TEXT"),                print(f"❌ Image generation failed: {response.status_code}")        os.makedirs(self.data_dir, exist_ok=True)            "temperature": 0.5,

                  ("tags", "TEXT"), ("meta_description", "TEXT"), ("image_data", "TEXT"),

                  ("content_generated", "INTEGER DEFAULT 0"), ("generated_at", "TIMESTAMP")]        except Exception as e:

        

        for column_name, column_type in columns:            print(f"❌ Image generation error: {str(e)}")                "maxOutputTokens": 1000

            try:

                cursor.execute(f"ALTER TABLE candidates ADD COLUMN {column_name} {column_type}")        

            except sqlite3.OperationalError:

                pass        return None    def call_gemini(self, prompt, model="gemini-1.5-flash"):        }

        

        # Save to database    

        cursor.execute("""

            UPDATE candidates     def generate_content_with_gemini(self, title, snippet, suggested_angle):        """    }

            SET generated_title = ?, excerpt = ?, content = ?, tags = ?, 

                meta_description = ?, image_data = ?, content_generated = 1,        """Generate blog content using Gemini 2.5."""

                generated_at = CURRENT_TIMESTAMP

            WHERE id = ?        prompt = f"""        Calls Gemini API with a prompt.    response = requests.post(url, headers=headers, json=data)

        """, (content_data['title'], content_data['excerpt'], content_data['content'],

              ','.join(content_data['tags']), content_data['meta_description'],         Write a comprehensive blog post for "Unravel" - a technology blog.

              image_data, candidate_id))

                        Returns the generated text.    if response.status_code == 200:

        conn.commit()

        conn.close()        Title: {title}

        

        # Save content to markdown file        Description: {snippet}        """        result = response.json()

        data_dir = os.path.dirname(self.db_path)

        filename = f"post_{candidate_id}.md"        Angle: {suggested_angle}

        filepath = os.path.join(data_dir, filename)

                        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.gemini_api_key}"        if 'candidates' in result and len(result['candidates']) > 0:

        with open(filepath, 'w', encoding='utf-8') as f:

            f.write(f"# {content_data['title']}\n\n")        Requirements:

            f.write(f"**Excerpt:** {content_data['excerpt']}\n\n")

            f.write(f"**Tags:** {', '.join(content_data['tags'])}\n\n")        1. Engaging introduction that hooks readers        headers = {"Content-Type": "application/json"}            return result['candidates'][0]['content']['parts'][0]['text']

            f.write(f"**Meta Description:** {content_data['meta_description']}\n\n")

            f.write("---\n\n")        2. Well-structured content with clear sections

            f.write(content_data['content'])

                3. Practical insights and actionable takeaways        data = {        else:

        print(f"💾 Content saved: {filename}")

        return filepath        4. Professional tone but accessible language

    

    def write_content(self, limit=3):        5. Include relevant examples and use cases            "contents": [{            print("No content in Gemini response:", result)

        """Generate content for validated candidates."""

        print("✍️ Starting content generation phase...")        6. Strong conclusion that summarizes key points

        candidates = self.get_validated_candidates(limit)

                7. Length: 800-1200 words                "parts": [{"text": prompt}]            return None

        if not candidates:

            print("📊 No candidates ready for content generation")        8. Use markdown formatting

            return 0

                            }],    else:

        generated_count = 0

        for candidate in candidates:        Structure the response as a JSON object:

            print(f"✍️ Writing content for: {candidate['title'][:50]}...")

                    {{            "generationConfig": {        print("Gemini error:", response.text)

            content = self.generate_content_with_gemini(candidate['title'], candidate['snippet'], candidate['suggested_angle'])

                        "title": "Compelling blog post title",

            if content:

                # Generate image (placeholder for now)            "excerpt": "Brief excerpt for preview (150 characters max)",                "temperature": 0.7,        return None

                image_data = self.generate_image(content.get('image_prompt', candidate['title']))

                self.save_generated_content(candidate['id'], content, image_data)            "content": "Full markdown content",

                generated_count += 1

                print(f"✅ Content generated for candidate {candidate['id']}")            "tags": ["tag1", "tag2", "tag3"],                "maxOutputTokens": 2000

            else:

                print(f"❌ Failed to generate content for candidate {candidate['id']}")            "meta_description": "SEO meta description (160 characters max)",

        

        print(f"📊 Content generation complete: {generated_count}/{len(candidates)} posts written")            "image_prompt": "Descriptive prompt for generating a header image"            }# -------------------------------

        return generated_count

            }}

    def get_writing_stats(self):

        """Get content generation statistics."""        """        }# Build prompt

        conn = sqlite3.connect(self.db_path)

        cursor = conn.cursor()        

        

        try:        headers = {        # -------------------------------

            cursor.execute("SELECT COUNT(*) FROM candidates WHERE content_generated=1")

            total_written = cursor.fetchone()[0]            'Content-Type': 'application/json',

            

            cursor.execute("SELECT COUNT(*) FROM candidates WHERE content_generated=1 AND image_data IS NOT NULL")        }        response = requests.post(url, headers=headers, json=data)def build_prompt(candidate):

            with_images = cursor.fetchone()[0]

                    

            cursor.execute("SELECT COUNT(*) FROM candidates WHERE validated=1 AND content_generated=0")

            ready_to_write = cursor.fetchone()[0]        data = {        if response.status_code == 200:    return f"""

        except sqlite3.OperationalError:

            total_written = with_images = ready_to_write = 0            "contents": [{

        

        conn.close()                "parts": [{            result = response.json()System: You are BlogWriter-Gemini. Output ONLY Markdown with YAML front matter.

        return {'total_written': total_written, 'with_images': with_images, 'ready_to_write': ready_to_write}

                    "text": prompt

def main():

    """Run the writer agent standalone."""                }]            if 'candidates' in result and len(result['candidates']) > 0:

    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sqlite.db')

    gemini_api_key = os.getenv('GEMINI_API_KEY')            }],

    

    if not gemini_api_key:            "generationConfig": {                return result['candidates'][0]['content']['parts'][0]['text']User: Write a ~800 word blog post.

        print("❌ GEMINI_API_KEY environment variable not set")

        return                "temperature": 0.7,

    

    agent = WriterAgent(db_path, gemini_api_key)                "topK": 40,            else:Title: {candidate['title']}

    stats = agent.get_writing_stats()

    print(f"📊 Writing stats: {stats}")                "topP": 0.95,

    agent.write_content(limit=3)

    stats = agent.get_writing_stats()                "maxOutputTokens": 4096,                print("No content in Gemini response:", result)Tone: casual

    print(f"📊 Updated writing stats: {stats}")

            }

if __name__ == "__main__":

    main()        }                return NoneKeywords: AI, blogging

        

        try:        else:Evidence summary: score={candidate['score']}, snippet="{candidate['snippet']}"

            response = requests.post(

                f"{self.api_endpoint}?key={self.gemini_api_key}",            print("Gemini API error:", response.text)

                headers=headers,

                json=data,            return NoneRequirements:

                timeout=60

            )    - Start with YAML front matter between --- delimiters (not code blocks)

            

            if response.status_code == 200:    def build_writing_prompt(self, candidate):- Include title, meta_description, tags in YAML

                result = response.json()

                text = result['candidates'][0]['content']['parts'][0]['text']        """Build writing prompt for Gemini."""- Follow with markdown content

                

                # Extract JSON from response        return f"""- Use headings, examples, conclusion

                try:

                    start = text.find('{')System: You are BlogWriter-Gemini. Output ONLY Markdown with YAML front matter.- Add a sources section at the end

                    end = text.rfind('}') + 1

                    json_str = text[start:end]

                    content_result = json.loads(json_str)

                    return content_resultUser: Write a ~800 word blog post.Example format:

                except (json.JSONDecodeError, ValueError):

                    print("❌ Failed to parse content JSON")Title: {candidate['title']}---

                    return None

            else:Tone: casual, engaging, informativetitle: "Your Title Here"

                print(f"❌ Content generation failed: {response.status_code}")

                return NoneKeywords: AI, blogging, technology, innovationmeta_description: "Brief description"

                

        except Exception as e:Evidence summary: score={candidate['score']}, snippet="{candidate['snippet']}"tags: ["AI", "blogging", "technology"]

            print(f"❌ Content generation error: {str(e)}")

            return Nonefeatured_image: "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=1200&h=600&fit=crop"

    

    def get_validated_candidates(self, limit=5):Requirements:---

        """Get validated candidates that haven't been written yet."""

        conn = sqlite3.connect(self.db_path)- Start with YAML front matter between --- delimiters (not code blocks)

        cursor = conn.cursor()

        - Include title, meta_description, tags in YAML# Your Title Here

        # Check if content_generated column exists, if not add it

        try:- Follow with markdown content including an image at the top

            cursor.execute("ALTER TABLE candidates ADD COLUMN content_generated INTEGER DEFAULT 0")

        except sqlite3.OperationalError:- Use headings, examples, practical tips, conclusionYour content here...

            pass  # Column already exists

        - Add a sources section at the end

        cursor.execute("""

            SELECT id, title, snippet, suggested_angle, score- Make it engaging and actionable## Conclusion

            FROM candidates 

            WHERE validated = 1 AND content_generated = 0 AND score >= 6

            ORDER BY score DESC, created_at ASC

            LIMIT ?Example format:...

        """, (limit,))

        ---

        candidates = cursor.fetchall()

        conn.close()title: "Your Title Here"## Sources

        

        return [meta_description: "Brief description under 160 characters"

            {

                'id': row[0],tags: ["AI", "blogging", "technology"]...

                'title': row[1],

                'snippet': row[2],---"""

                'suggested_angle': row[3] or 'General technology perspective',

                'score': row[4]

            }

            for row in candidates![Featured Image](https://via.placeholder.com/800x400/0066cc/ffffff?text=Blog+Post+Image)# -------------------------------

        ]

    # Generate Markdown

    def save_generated_content(self, candidate_id, content_data, image_data=None):

        """Save generated content to database and file."""# Your Title Here# -------------------------------

        conn = sqlite3.connect(self.db_path)

        cursor = conn.cursor()def write_post(candidate):

        

        # Add content columns if they don't existEngaging introduction paragraph that hooks the reader...    md = call_gemini(build_prompt(candidate))

        columns_to_add = [

            ("generated_title", "TEXT"),    return md

            ("excerpt", "TEXT"),

            ("content", "TEXT"),## Main Content Section

            ("tags", "TEXT"),

            ("meta_description", "TEXT"),# -------------------------------

            ("image_data", "TEXT"),

            ("content_generated", "INTEGER DEFAULT 0"),Your detailed content here with practical examples...# Generate for all validated but unpublished candidates

            ("generated_at", "TIMESTAMP")

        ]# -------------------------------

        

        for column_name, column_type in columns_to_add:## Another Sectiondef run_writer():

            try:

                cursor.execute(f"ALTER TABLE candidates ADD COLUMN {column_name} {column_type}")    conn = sqlite3.connect(DB_PATH)

            except sqlite3.OperationalError:

                pass  # Column already existsMore valuable content...    c = conn.cursor()

        

        # Save to database    c.execute("SELECT id, title, snippet, score FROM candidates WHERE validated=1 AND published=0")

        cursor.execute("""

            UPDATE candidates ## Conclusion    candidates = c.fetchall()

            SET generated_title = ?, excerpt = ?, content = ?, tags = ?, 

                meta_description = ?, image_data = ?, content_generated = 1,

                generated_at = CURRENT_TIMESTAMP

            WHERE id = ?Wrap up with key takeaways and actionable insights...    for cand in candidates:

        """, (

            content_data['title'],        candidate = {"id": cand[0], "title": cand[1], "snippet": cand[2], "score": cand[3]}

            content_data['excerpt'],

            content_data['content'],## Sources        md = write_post(candidate)

            ','.join(content_data['tags']),

            content_data['meta_description'],        if md:

            image_data,

            candidate_id- Reference sources and additional reading            # store Markdown temporarily in DB or file using correct path

        ))

                    data_dir = os.path.join(script_dir, '..', 'data')

        conn.commit()

        conn.close()IMPORTANT: Include an image right after the YAML frontmatter using markdown format:            post_file = os.path.join(data_dir, f"post_{candidate['id']}.md")

        

        # Save content to markdown file![Tech News](https://via.placeholder.com/800x400/0066cc/ffffff?text=Tech+News)            with open(post_file, "w", encoding="utf-8") as f:

        data_dir = os.path.join(os.path.dirname(self.db_path))

        filename = f"post_{candidate_id}.md"                f.write(md)

        filepath = os.path.join(data_dir, filename)

        Make the content valuable, actionable, and engaging for readers interested in technology and innovation.            print(f"Written post: {candidate['title']}")

        with open(filepath, 'w', encoding='utf-8') as f:

            f.write(f"# {content_data['title']}\n\n")"""

            f.write(f"**Excerpt:** {content_data['excerpt']}\n\n")

            f.write(f"**Tags:** {', '.join(content_data['tags'])}\n\n")        conn.close()

            f.write(f"**Meta Description:** {content_data['meta_description']}\n\n")

            f.write("---\n\n")    def write_post(self, candidate):

            f.write(content_data['content'])

                """Generate markdown content for a candidate."""# -------------------------------

        print(f"💾 Content saved: {filename}")

        return filepath        prompt = self.build_writing_prompt(candidate)if __name__ == "__main__":

    

    def write_content(self, limit=3):        md_content = self.call_gemini(prompt)    run_writer()

        """Generate content for validated candidates."""        return md_content

        print("✍️ Starting content generation phase...")    

            def get_validated_unpublished_candidates(self):

        candidates = self.get_validated_candidates(limit)        """Get all validated but unpublished candidates."""

        if not candidates:        conn = sqlite3.connect(self.db_path)

            print("📊 No candidates ready for content generation")        cursor = conn.cursor()

            return 0        

                cursor.execute("SELECT id, title, snippet, score FROM candidates WHERE validated=1 AND published=0")

        generated_count = 0        candidates = cursor.fetchall()

                

        for candidate in candidates:        conn.close()

            print(f"✍️ Writing content for: {candidate['title'][:50]}...")        

                    return [

            # Generate content            {"id": cand[0], "title": cand[1], "snippet": cand[2], "score": cand[3]}

            content = self.generate_content_with_gemini(            for cand in candidates

                candidate['title'],        ]

                candidate['snippet'],    

                candidate['suggested_angle']    def save_post_to_file(self, candidate_id, title, content):

            )        """Save generated content to markdown file."""

                    post_file = os.path.join(self.data_dir, f"post_{candidate_id}.md")

            if content:        

                # Generate image        try:

                print("🎨 Generating header image...")            with open(post_file, "w", encoding="utf-8") as f:

                image_data = self.generate_image(content.get('image_prompt', candidate['title']))                f.write(content)

                            

                # Save content            print(f"✓ Saved: {title[:50]}... → {post_file}")

                self.save_generated_content(candidate['id'], content, image_data)            return True

                generated_count += 1        except Exception as e:

                            print(f"❌ Failed to save {title[:50]}...: {str(e)}")

                print(f"✅ Content generated for candidate {candidate['id']}")            return False

            else:    

                print(f"❌ Failed to generate content for candidate {candidate['id']}")    def run_writer(self, limit=None):

                """Generate content for all validated but unpublished candidates."""

        print(f"📊 Content generation complete: {generated_count}/{len(candidates)} posts written")        print("✍️ Running writer agent...")

        return generated_count        

            candidates = self.get_validated_unpublished_candidates()

    def get_writing_stats(self):        

        """Get content generation statistics."""        if not candidates:

        conn = sqlite3.connect(self.db_path)            print("📭 No candidates to write content for.")

        cursor = conn.cursor()            return 0

                

        try:        if limit:

            cursor.execute("SELECT COUNT(*) FROM candidates WHERE content_generated=1")            candidates = candidates[:limit]

            total_written = cursor.fetchone()[0]        

                    written_count = 0

            cursor.execute("SELECT COUNT(*) FROM candidates WHERE content_generated=1 AND image_data IS NOT NULL")        

            with_images = cursor.fetchone()[0]        for candidate in candidates:

                        print(f"✍️ Writing: {candidate['title'][:50]}...")

            cursor.execute("SELECT COUNT(*) FROM candidates WHERE validated=1 AND content_generated=0")            

            ready_to_write = cursor.fetchone()[0]            md_content = self.write_post(candidate)

        except sqlite3.OperationalError:            

            # Handle case where columns don't exist yet            if md_content:

            total_written = 0                if self.save_post_to_file(candidate['id'], candidate['title'], md_content):

            with_images = 0                    written_count += 1

            ready_to_write = 0                    print(f"✓ Written: {candidate['title'][:50]}...")

                        else:

        conn.close()                    print(f"❌ Failed to save: {candidate['title'][:50]}...")

                    else:

        return {                print(f"❌ Failed to generate content: {candidate['title'][:50]}...")

            'total_written': total_written,        

            'with_images': with_images,        print(f"📝 Writing complete: {written_count} posts written")

            'ready_to_write': ready_to_write        return written_count

        }    

    def get_writing_stats(self):

def main():        """Get writing statistics."""

    """Run the writer agent standalone."""        conn = sqlite3.connect(self.db_path)

    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sqlite.db')        cursor = conn.cursor()

            

    # Get API key from environment        cursor.execute("SELECT COUNT(*) FROM candidates WHERE validated=1 AND published=0")

    gemini_api_key = os.getenv('GEMINI_API_KEY')        ready_to_write = cursor.fetchone()[0]

    if not gemini_api_key:        

        print("❌ GEMINI_API_KEY environment variable not set")        conn.close()

        return        

            # Count existing markdown files

    agent = WriterAgent(db_path, gemini_api_key)        written_files = 0

            if os.path.exists(self.data_dir):

    # Show current stats            written_files = len([f for f in os.listdir(self.data_dir) if f.startswith('post_') and f.endswith('.md')])

    stats = agent.get_writing_stats()        

    print(f"📊 Writing stats: {stats}")        return {

                'ready_to_write': ready_to_write,

    # Generate content            'written_files': written_files

    agent.write_content(limit=3)        }

    

    # Show updated statsdef main():

    stats = agent.get_writing_stats()    """Run the writer agent standalone."""

    print(f"📊 Updated writing stats: {stats}")    script_dir = os.path.dirname(__file__)

    db_path = os.path.join(script_dir, '..', 'data', 'sqlite.db')

if __name__ == "__main__":    data_dir = os.path.join(script_dir, '..', 'data')

    main()    
    agent = WriterAgent(db_path, data_dir)
    
    # Show current stats
    stats = agent.get_writing_stats()
    print(f"📊 Writing stats: {stats}")
    
    # Generate content (limit to 3 for testing)
    written = agent.run_writer(limit=3)
    
    # Show updated stats
    stats = agent.get_writing_stats()
    print(f"📊 Updated stats: {stats}")

if __name__ == "__main__":
    main()