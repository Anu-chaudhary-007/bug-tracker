import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS bugs(
    id INTEGER PRIMARY KEY  AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT DEFAULT 'Open',
    reported_by TEXT NOT NULL
)
''')
conn.commit()
conn.close()

print("🛠️ Bugs table created.")