import sqlite3

def init_db():
    conn = sqlite3.connect('happylivein.db')
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create customers table
    c.execute('''
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
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('happylivein', 'shikhar'))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
