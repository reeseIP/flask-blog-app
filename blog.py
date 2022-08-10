'''
WARNING: Make the value of your secret key really, really hard, if not impossible,
to guess. Use a random key generator to do this. Never, ever use a value you pick
on your own. Or you can use your OS to get a random string:
>>> import os
>>> os.urandom(24)
'rM\xb1\xdc\x12o\xd6i\xff+9$T\x8e\xec\x00\x13\x82.*\x16TG\xbd'
Now you can simply assign that string to the secret key: SECRET_KEY =
rM\xb1\xdc\x12o\xd6i\xff+9$T\x8e\xec\x00\x13\x82.*\x16TG\xbd
'''
# imports
from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, g
from functools import wraps
import sqlite3

# config
DATABASE = 'D:/Real Python Material/Repositories/flask-blog-app/blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'hard_to_guess'

app = Flask(__name__)

# pulls in app config by looking for UPPERCASE variables
app.config.from_object(__name__)

# function used for connecting to the DB
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
    
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to log in first.')
            return redirect(url_for('login'))
    return wrap
    
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    status_code = 200
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
            request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            status_code = 401
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html',error=error), status_code
    
@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    content = request.form['content']
    if not title or not content:
        flash('All fields are required. Please check your entry')
        return redirect(url_for('main'))
    else:
        g.db = connect_db()
        g.db.execute('INSERT INTO posts(title,content) VALUES(?,?)', [request.form['title'], request.form['content']])
        g.db.commit()
        g.db.close()
        flash('New entry was successfully posted!')
        return redirect(url_for('main'))
    
@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('You were logged out')
    return redirect(url_for('login'))
    
@app.route('/main')
@login_required
def main():
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM posts')
    posts = [dict(title=row[0], content=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('main.html',posts=posts)
    
if __name__ == '__main__':
    app.run(debug=True)