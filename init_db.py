import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'happylivein.db')

def init_db():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)  # Delete old database if exists

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Insert default user
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('happylivein', 'shikhar'))

    # Create customers table
    c.execute('''
        CREATE TABLE customers (
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

    conn.commit()
    conn.close()
    print("Database initialized with default user.")

if __name__ == '__main__':
    init_db()
