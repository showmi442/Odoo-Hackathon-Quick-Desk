from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'quickdesk_secret'
DB_PATH = 'database/quickdesk.db'

# Ensure database folder exists
os.makedirs('database', exist_ok=True)

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')

    # Tickets table
    c.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            description TEXT,
            category TEXT,
            status TEXT DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Comments table
    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER,
            user_id INTEGER,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(ticket_id) REFERENCES tickets(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# ---------- Routes ---------- #

@app.route('/')
def index():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']

        conn = sqlite3.connect(DB_PATH)
        try:
            conn.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)", (name, email, password, role))
            conn.commit()
            flash('Registration successful. Please log in.')
            return redirect('/login')
        except:
            flash('Email already registered.')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect(DB_PATH)
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['role'] = user[4]
            return redirect('/dashboard')
        else:
            flash('Invalid credentials')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect(DB_PATH)
    if session['role'] == 'enduser':
        tickets = conn.execute("SELECT * FROM tickets WHERE user_id = ?", (session['user_id'],)).fetchall()
    else:
        tickets = conn.execute("SELECT * FROM tickets").fetchall()
    conn.close()

    return render_template('dashboard.html', tickets=tickets)

@app.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        subject = request.form['subject']
        description = request.form['description']
        category = request.form['category']

        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO tickets (user_id, subject, description, category) VALUES (?, ?, ?, ?)",
                     (session['user_id'], subject, description, category))
        conn.commit()
        conn.close()
        flash('Ticket submitted successfully!')
        return redirect('/dashboard')

    return render_template('create_ticket.html')

@app.route('/ticket/<int:id>', methods=['GET', 'POST'])
def ticket_detail(id):
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect(DB_PATH)
    ticket = conn.execute("SELECT * FROM tickets WHERE id = ?", (id,)).fetchone()
    comments = conn.execute(
        "SELECT comments.message, users.name, comments.created_at FROM comments JOIN users ON comments.user_id = users.id WHERE ticket_id = ? ORDER BY comments.created_at ASC",
        (id,)
    ).fetchall()

    if request.method == 'POST':
        if request.form.get('action') == 'update_status':
            new_status = request.form['status']
            conn.execute("UPDATE tickets SET status = ? WHERE id = ?", (new_status, id))
            conn.commit()
            conn.close()
            return redirect(f'/ticket/{id}')
        else:
            msg = request.form['message']
            conn.execute("INSERT INTO comments (ticket_id, user_id, message) VALUES (?, ?, ?)", (id, session['user_id'], msg))
            conn.commit()
            conn.close()
            return redirect(f'/ticket/{id}')

    conn.close()
    return render_template('ticket_detail.html', ticket=ticket, comments=comments)

# ---------- Run ---------- #
if __name__ == '__main__':
    app.run(debug=True)
