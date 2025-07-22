import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'happylivein.db')

def init_db():
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

    # Insert default user (your credentials)
    cursor.execute('DELETE FROM users')  # Clean old users
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('happylivein', 'shikhar'))

    conn.commit()
    conn.close()
    print("Database initialized with default user.")

if __name__ == '__main__':
    init_db()
