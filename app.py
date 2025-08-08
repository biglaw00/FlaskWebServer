from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'biglaw00'

def init_db():
    conn = sqlite3.connect('user.db')
    cur = conn.cursor()
    cur.execute('''
                   CREATE TABLE IF NOT EXISTS users (
                   id TEXT PRIMAY KEY, 
                   pw TEXT NOT NULL
                   )
            ''')
    conn.commit()
    conn.close()
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contract')
def contract():
    return render_template('contract.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        uid = request.form['id']
        pw = request.form['pw']

        conn = sqlite3.connect('user.db')
        cur = conn.cursor()
        try :
            cur.execute('INSERT INTO users(id,pw) VALUES(?,?)',(uid,pw))
            conn.commit()
        except sqlite3.IntegrityError :
            conn.close()
            return "이미 존재하는 ID입니다."
        conn.close()
        return redirect('/login')
    else :
        return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        uid = request.form['id']
        pw = request.form['pw']

        conn = sqlite3.connect('user.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE id=? AND pw=?',(uid,pw))
        user = cur.fetchone()
        conn.close()

        if user:
            session ['user'] = uid
            return redirect('/')
        else :
            return "id 혹은 pw가 틀렸습니다."
    
    return render_template('login.html')

if __name__ == '__main__' :
    app.run(debug=True,use_reloader=True)    