import os
if not os.path.exists(DATABASE):
    from init_db import init_db
    init_db()

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = "/tmp/happylivein.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return redirect(url_for('login'))

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
            flash('Invalid credentials')
            return redirect(url_for('login'))

    return render_template('login.html')

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

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer_route():
    if 'user_id' not in session:
        return redirect(url_for('login'))

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

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO customers (
                date, client_name, location, mode, notes,
                next_followup, meeting_notes, address, property_size,
                requirement, possession, budget, quotation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tuple(data.values()))
        conn.commit()
        conn.close()

        flash('Customer added successfully!')
        return redirect(url_for('dashboard'))

    return render_template('add_customer.html')

@app.route('/edit_customer/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    customer = conn.execute('SELECT * FROM customers WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        updated_data = {
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

        conn.execute('''
            UPDATE customers SET
                date = ?, client_name = ?, location = ?, mode = ?, notes = ?,
                next_followup = ?, meeting_notes = ?, address = ?, property_size = ?,
                requirement = ?, possession = ?, budget = ?, quotation = ?
            WHERE id = ?
        ''', tuple(updated_data.values()) + (id,))
        conn.commit()
        conn.close()
        flash('Customer updated successfully!')
        return redirect(url_for('dashboard'))

    conn.close()
    return render_template('edit_customer.html', customer=customer)

@app.route('/delete_customer/<int:id>')
def delete_customer(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute('DELETE FROM customers WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Customer deleted successfully!')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
