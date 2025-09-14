import sqlite3

conn = sqlite3.connect("clue_trail.db")
cursor = conn.cursor()

# Check if the column exists
cursor.execute('PRAGMA table_info("case")')  # <-- put table name in quotes
columns = [col[1] for col in cursor.fetchall()]

if "date_added" not in columns:
    cursor.execute("""
        ALTER TABLE "case"
        ADD COLUMN date_added DATETIME DEFAULT CURRENT_TIMESTAMP
    """)
    print("date_added column added successfully.")
else:
    print("date_added column already exists.")

conn.commit()
conn.close()

