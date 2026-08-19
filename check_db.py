import sqlite3

conn = sqlite3.connect("staj.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT id, name, submitted_at
    FROM applications
    ORDER BY id DESC
""")

for row in cursor.fetchall():
    print(row)

conn.close()