import sqlite3

# Connect (creates file if not exists)
conn = sqlite3.connect('../data/sqlite.db')  # adjust path if needed
c = conn.cursor()

# Create table for candidate articles
c.execute('''
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    url TEXT,
    snippet TEXT,
    fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    validated INTEGER DEFAULT 0,
    score INTEGER,
    published INTEGER DEFAULT 0
)
''')

conn.commit()
conn.close()

print("SQLite DB and 'candidates' table created successfully!")