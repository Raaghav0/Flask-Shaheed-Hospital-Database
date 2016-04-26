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


#def init_db():
'''with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()'''









@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


class database:

    name=""
    email=""
    password=""
    phone_no=""
    Designation=""
d= []


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





    temp=database()
    temp.name =request.form["Name"]
    temp.password=request.form["pwd"]
    temp.Designation=request.form["designation"]
    temp.phone_no=request.form["pno"]
    temp.email=request.form["email"]
    db.execute('insert into entries (name, emailid, password, Designation, phone_no) values (?, ?, ?, ?, ?)',
               [request.form["Name"],request.form["email"],request.form["pwd"] ,request.form["designation"],request.form["pno"]])
    db.commit()
    d.append(temp)
    #  print(db[0])



    return redirect(url_for('login'))

@app.route('/loggedin/',methods=['POST'])
def loggedin():
    if request.form['username']==d[0].name and request.form['pwd']==d[0].password:
        return render_template("index.html")
    return render_template("login.html")





@app.route('/outpatient/')
def outpatient():
    return render_template("outpatient.html")
@app.route('/outpatient/addpatient/')
def addpatient():
    return render_template("addpatient.html")

@app.route('/show/')
def show_entries():

    cur = g.db.execute('select name, password from entries order by id desc')
    entries = [dict(title=row[0], text=row[2]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

if __name__ == '__main__':
   #init_db()
   with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
   app.run(debug=True)

