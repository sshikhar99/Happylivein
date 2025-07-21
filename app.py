from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

DATABASE = 'crm.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        else:
            return render_template('home.html', error='Invalid credentials')
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM customers ORDER BY id DESC').fetchall()
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
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO customers (date, client_name, location, mode, notes, next_followup, meeting_notes,
                                   address, property_size, requirement, possession, budget, quotation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))

    return render_template('add_customer.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    customer = conn.execute('SELECT * FROM customers WHERE id = ?', (id,)).fetchone()

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
            request.form['quotation'],
            id
        )
        conn.execute('''
            UPDATE customers
            SET date=?, client_name=?, location=?, mode=?, notes=?, next_followup=?, meeting_notes=?,
                address=?, property_size=?, requirement=?, possession=?, budget=?, quotation=?
            WHERE id=?
        ''', data)
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))

    conn.close()
    return render_template('edit_customer.html', customer=customer)

@app.route('/delete/<int:id>')
def delete_customer(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    conn.execute('DELETE FROM customers WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
