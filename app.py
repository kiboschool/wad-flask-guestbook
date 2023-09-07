from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
DATABASE = 'guestbook.db'
app.secret_key = '123'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS guests (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                message TEXT NOT NULL
            )
        """)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Server-side validation
        if not name or not email or not message:
            flash('Please fill in all fields!')
            return redirect(url_for('index'))

        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO guests (name, email, message) VALUES (?, ?, ?)", (name, email, message))
            conn.commit()

        flash('Guest entry added successfully!')

    # Retrieve all guest entries for display
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT name, email, message FROM guests")
        guests = cur.fetchall()

    return render_template('index.html', guests=guests)