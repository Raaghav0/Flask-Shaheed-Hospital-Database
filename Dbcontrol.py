from sqlite3 import dbapi2 as sqlite3
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash,get_flashed_messages
from contextlib import closing
import os
app=Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()









'''@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()'''

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login/')
def login():
    return render_template("login.html")

@app.route('/signup/')
def signup():
 return render_template("signup.html")
@app.route('/signedup/',methods=['POST'])
def signedup():
        # if not session.get('logged_in'):
        #abort(401)
    db=get_db()
    db.execute('insert into entries (name, emailid, password, Designation, phone_no) values (?, ?, ?, ?, ?)',
        [request.form['Name'], request.form['email'],request.form['pwd'],request.form['designation'],request.form['pno']])
    db.commit()
    return redirect(url_for('login'))




@app.route('/outpatient/')
def outpatient():
    return render_template("outpatient.html")
@app.route('/outpatient/addpatient/')
def addpatient():
    return render_template("addpatient.html")

if __name__ == '__main__':
   app.run(debug=True)
   init_db()
