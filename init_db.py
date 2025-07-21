import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('crm.db')
c = conn.cursor()

# Drop existing tables for a clean reset (optional)
c.execute('DROP TABLE IF EXISTS users')
c.execute('DROP TABLE IF EXISTS customers')

# Create users table
c.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

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
    quotation TEXT CHECK (quotation IN ('Yes', 'No'))
)
''')

# Add default admin user (username: admin, password: admin123)
hashed_password = generate_password_hash('admin123')
c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', hashed_password))

conn.commit()
conn.close()

print("✅ Database initialized successfully.")
