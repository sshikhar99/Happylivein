from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'happylivein_secret'

DATABASE = os.path.join(os.path.dirname(__file__), 'happylivein.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return render_template('dashboard.html', customers=customers)

@app.route('/delete/<int:id>')
def delete_customer_route(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM customers WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer_route():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = [request.form.get(field) for field in [
            'date', 'client_name', 'location', 'mode', 'notes',
            'next_followup', 'meeting_notes', 'address', 'property_size',
            'requirement', 'possession', 'budget', 'quotation'
        ]]
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO customers (
                date, client_name, location, mode, notes,
                next_followup, meeting_notes, address, property_size,
                requirement, possession, budget, quotation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))

    return render_template('add_customer.html')

@app.route('/edit_customer/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    customer = conn.execute('SELECT * FROM customers WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        data = [request.form.get(field) for field in [
            'date', 'client_name', 'location', 'mode', 'notes',
            'next_followup', 'meeting_notes', 'address', 'property_size',
            'requirement', 'possession', 'budget', 'quotation'
        ]]
        data.append(id)
        conn.execute('''
            UPDATE customers SET
                date=?, client_name=?, location=?, mode=?, notes=?,
                next_followup=?, meeting_notes=?, address=?, property_size=?,
                requirement=?, possession=?, budget=?, quotation=?
            WHERE id=?
        ''', data)
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))

    conn.close()
    return render_template('edit_customer.html', customer=customer)

if __name__ == '__main__':
    app.run()
