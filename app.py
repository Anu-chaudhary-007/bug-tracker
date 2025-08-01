from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in real apps

# Home route
@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))


# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()  
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid credentials"

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)  # ✅ Fixed: typo in 'username'
    return redirect(url_for('login'))

# Bug report route
@app.route('/report', methods=['GET', 'POST'])
def report_bug():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        reported_by = session['username']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bugs (title, description, reported_by) VALUES (?, ?, ?)',
                       (title, description, reported_by))
        conn.commit()
        conn.close()

        return render_template("success.html")


    return render_template('report.html')

# Bug dashboard route
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    status_filter = request.args.get('status')
    my_bugs = request.args.get('my') == 'true'
    search_query = request.args.get('query')
    username = session['username']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    base_query = "SELECT * FROM bugs WHERE 1=1"
    params = []

    if my_bugs:
        base_query += " AND reported_by = ?"
        params.append(username)

    if status_filter:
        base_query += " AND status = ?"
        params.append(status_filter)

    if search_query:
        base_query += " AND (title LIKE ? OR description LIKE ?)"
        like_term = f"%{search_query}%"
        params.extend([like_term, like_term])

    cursor.execute(base_query, params)
    bugs = cursor.fetchall()
    conn.close()

    return render_template('dashboard.html', bugs=bugs)

# delete route    
@app.route('/delete/<int:bug_id>')
def delete_bug(bug_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM bugs WHERE id = ?', (bug_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))
    
#edit & delete bug
@app.route('/edit/<int:bug_id>', methods=['GET', 'POST'])
def edit_bug(bug_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']

        cursor.execute('''
            UPDATE bugs
            SET title = ?, description = ?, status = ?
            WHERE id = ?
        ''', (title, description, status, bug_id))

        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))

    # GET method: fetch the bug to edit
    cursor.execute('SELECT * FROM bugs WHERE id = ?', (bug_id,))
    bug = cursor.fetchone()
    conn.close()

    return render_template('edit.html', bug=bug)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

