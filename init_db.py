import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# USERS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# GOALS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS goals(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    goal TEXT,
    days INTEGER
)
""")

conn.commit()
conn.close()

print("Database updated!")