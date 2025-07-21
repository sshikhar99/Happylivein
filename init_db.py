import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'happylivein.db')

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            client_name TEXT,
            location TEXT,
            mode TEXT,
            notes TEXT,
            next_followup TEXT,
            meeting_notes TEXT,
            address TEXT,
            property_size TEXT,
            requirement TEXT,
            possession TEXT,
            budget TEXT,
            quotation TEXT
        )
    ''')

    # Insert default user
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'admin123'))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
