import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = 'happylivein.db'

# Connect to the database
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Drop existing tables (optional, for clean re-init)
cursor.execute('DROP TABLE IF EXISTS users')
cursor.execute('DROP TABLE IF EXISTS customers')

# Create users table
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Insert default admin user
admin_username = 'admin'
admin_password = generate_password_hash('admin')
cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (admin_username, admin_password))

# Create customers table
cursor.execute('''
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

# Commit changes and close connection
conn.commit()
conn.close()

print("Database initialized successfully with default admin.")
