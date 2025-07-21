import sqlite3
import os

DATABASE = 'happylivein.db'

def init_db():
    # Ensure old DB is removed (optional)
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Create customers table
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

    # Insert default admin user
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)
    ''', ('admin', 'admin'))

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
