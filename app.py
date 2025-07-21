from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

import os
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(basedir, 'crm.db')


# Initialize DB if not exists
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL)''')

        c.execute('''CREATE TABLE IF NOT EXISTS customers (
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
                        quotation TEXT)''')

        # Default user
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'admin'))
        conn.commit()
        conn.close()

init_db()

# ---------------------- ROUTES ----------------------

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid Credentials'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM customers")
    customers = c.fetchall()
    conn.close()
    return render_template('dashboard.html', customers=customers)

@app.route('/add', methods=['GET', 'POST'])
def add_customer():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = (
            request.form['date'],
            request.form['client_name'],
            request.form['location'],
            request.form['mode'],
            request.form['notes'],
            request.form['next_followup'],
            request.form['meeting_notes'],
            request.form['address'],
            request.form['property_size'],
            request.form['requirement'],
            request.form['possession'],
            request.form['budget'],
            request.form['quotation']
        )

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''INSERT INTO customers (
            date, client_name, location, mode, notes, next_followup, meeting_notes,
            address, property_size, requirement, possession, budget, quotation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))

    return render_template('add_customer.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    if request.method == 'POST':
        updated_data = (
            request.form['date'],
            request.form['client_name'],
            request.form['location'],
            request.form['mode'],
            request.form['notes'],
            request.form['next_followup'],
            request.form['meeting_notes'],
            request.form['address'],
            request.form['property_size'],
            request.form['requirement'],
            request.form['possession'],
            request.form['budget'],
            request.form['quotation'],
            id
        )

        c.execute('''UPDATE customers SET
            date=?, client_name=?, location=?, mode=?, notes=?, next_followup=?,
            meeting_notes=?, address=?, property_size=?, requirement=?, possession=?,
            budget=?, quotation=? WHERE id=?''', updated_data)

        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))

    c.execute("SELECT * FROM customers WHERE id=?", (id,))
    customer = c.fetchone()
    conn.close()
    return render_template('edit_customer.html', customer=customer)

@app.route('/delete/<int:id>')
def delete_customer(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM customers WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

# ---------------------- MAIN ----------------------

if __name__ == '__main__':
    app.run(debug=True)
