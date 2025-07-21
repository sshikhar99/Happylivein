from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# ✅ Define DATABASE path at the top before usage
DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'happylivein.db')

# Optional: If you want to make sure the file exists on Render before anything runs (prevent error)
if not os.path.exists(DATABASE):
    open(DATABASE, 'a').close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials'
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return render_template('dashboard.html', customers=customers)

@app.route('/add', methods=['GET', 'POST'])
def add_customer_route():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        form_data = (
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
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO customers (date, client_name, location, mode, notes, next_followup, meeting_notes,
                                   address, property_size, requirement, possession, budget, quotation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', form_data)
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_customer.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    customer = conn.execute('SELECT * FROM customers WHERE id = ?', (id,)).fetchone()

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
        conn.execute('''
            UPDATE customers
            SET date = ?, client_name = ?, location = ?, mode = ?, notes = ?, next_followup = ?,
                meeting_notes = ?, address = ?, property_size = ?, requirement = ?, possession = ?,
                budget = ?, quotation = ?
            WHERE id = ?''', updated_data)
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))

    conn.close()
    return render_template('edit_customer.html', customer=customer)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_customer(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    conn.execute('DELETE FROM customers WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
