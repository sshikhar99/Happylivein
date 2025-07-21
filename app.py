from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# --- Database Helper Functions ---
def get_db_connection():
    conn = sqlite3.connect('crm.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_all_customers():
    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return customers

def add_customer(data):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO customers (date, client_name, location, mode, notes, next_followup, meeting_notes, address, property_size, requirement, possession, budget, quotation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['date'], data['client_name'], data['location'], data['mode'],
        data['notes'], data['next_followup'], data['meeting_notes'], data['address'],
        data['property_size'], data['requirement'], data['possession'], data['budget'], data['quotation']
    ))
    conn.commit()
    conn.close()

# --- Routes ---
@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['username'] = username
            return redirect('/dashboard')
        else:
            error = 'Invalid credentials'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        customers = get_all_customers()
        return render_template('dashboard.html', customers=customers)
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer_route():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        data = {
            'date': request.form['date'],
            'client_name': request.form['client_name'],
            'location': request.form['location'],
            'mode': request.form['mode'],
            'notes': request.form['notes'],
            'next_followup': request.form['next_followup'],
            'meeting_notes': request.form['meeting_notes'],
            'address': request.form['address'],
            'property_size': request.form['property_size'],
            'requirement': request.form['requirement'],
            'possession': request.form['possession'],
            'budget': request.form['budget'],
            'quotation': request.form['quotation']
        }
        add_customer(data)
        return redirect('/dashboard')

    return render_template('add_customer.html')

if __name__ == '__main__':
    app.run(debug=True)
