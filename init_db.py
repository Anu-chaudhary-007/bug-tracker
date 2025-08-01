import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         username TEXT NOT NULL UNIQUE,
         password TEXT NOT NULL
    )
''')
print("User table created successfully.")
conn.commit()
conn.close()

# Create bugs table
cursor.execute('''
CREATE TABLE IF NOT EXISTS bugs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    reported_by TEXT NOT NULL
)
''')

