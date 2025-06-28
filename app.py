from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)

songs_db = [
    {"mood": "bored", "language": "telugu", "title": "Samajavaragamana", "url": "/static/samajavaragamana.mp3"},
    {"mood": "bored", "language": "hindi", "title": "Kesariya", "url": "/static/kesariya.mp3"},
    {"mood": "bored", "language": "english", "title": "Shape of You", "url": "/static/shape_of_you.mp3"},
    {"mood": "happy", "language": "telugu", "title": "Butta Bomma", "url": "/static/butta_bomma.mp3"},
    {"mood": "happy", "language": "hindi", "title": "Gallan Goodiyan", "url": "/static/gallan_goodiyan.mp3"},
    {"mood": "happy", "language": "english", "title": "Happy", "url": "/static/happy.mp3"},
    {"mood": "sad", "language": "telugu", "title": "Nee Kallalona", "url": "/static/nee_kallalona.mp3"},
    {"mood": "sad", "language": "hindi", "title": "Channa Mereya", "url": "/static/channa_mereya.mp3"},
    {"mood": "sad", "language": "english", "title": "Someone Like You", "url": "/static/someone_like_you.mp3"},
    {"mood": "dj", "language": "telugu", "title": "Blockbuster", "url": "/static/blockbuster.mp3"},
    {"mood": "dj", "language": "hindi", "title": "Baby Doll", "url": "/static/baby_doll.mp3"},
    {"mood": "dj", "language": "english", "title": "Taki Taki", "url": "/static/taki_taki.mp3"},
    {"mood": "love failure", "language": "telugu", "title": "Inkem Inkem", "url": "/static/inkem_inkem.mp3"},
    {"mood": "love failure", "language": "hindi", "title": "Tadap Tadap", "url": "/static/tadap_tadap.mp3"},
    {"mood": "love failure", "language": "english", "title": "Let Her Go", "url": "/static/let_her_go.mp3"}
]

# Create users table
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Home - Redirect to register
@app.route('/')
def home():
    return redirect('/register')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            return redirect('/login')
        except sqlite3.IntegrityError:
            return "Username already exists!"
        finally:
            conn.close()

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()

        conn.close()

        if user:
            return redirect('/chatbot')
        else:
            return "Invalid Credentials."

    return render_template('login.html')

# Chatbot route
@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    filtered_songs = []

    if request.method == 'POST':
        mood = request.form.get('mood')
        language = request.form.get('language')

        filtered_songs = [song for song in songs_db if song['mood'] == mood and song['language'] == language]

    return render_template('index.html', songs=filtered_songs)

if __name__ == '__main__':
    app.run(debug=True)
