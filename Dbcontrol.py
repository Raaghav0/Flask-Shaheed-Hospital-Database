from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash,get_flashed_messages
from contextlib import closing
import os
import MySQLdb
from MySQLdb import escape_string as thwart
app=Flask(__name__)
app.secret_key="ABCD123"
from wtforms import Form , TextAreaField , PasswordField , validators
from passlib import hash

def connection():
    conn=MySQLdb.Connect(host="localhost",user="root",passwd="root",db="MYDB")
    c=conn.cursor()
    return c,conn


c, conn = connection()


class RegistrationForm(Form):
    username = TextAreaField('Username', [validators.Length(min=4, max=20)])
    email = TextAreaField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),validators.Length(min=5 ,max=20)
    ])
    confirm = PasswordField('Repeat Password')
    Designation = TextAreaField('Designation',[validators.DataRequired()])
    PhNumber = TextAreaField('Phone number',[validators.DataRequired()])

@app.route('/')
def index():
    session['invalid']=False
    return render_template("index.html")

@app.route('/login/')
def login():
    print session['invalid']
    if(session['invalid'] == True):
        flash("Invalid credentials")
    return render_template("login.html")


@app.route('/loggedin/',methods=["GET","POST"])
def loggedin():
    error = ''
    try:
        c, conn = connection()
        if request.method == "POST":

            data = c.execute("SELECT * FROM entries WHERE Username = '%s' " % thwart(request.form['username']))

            data = c.fetchone()[2]

            if hash.sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True

                session['username'] = request.form['username']
                print session['username']


                return redirect(url_for("outpatient"))

            else:
                session['invalid']=True
                return redirect(url_for("login"))

    except Exception as e:
        # flash(e)
        error = "Invalid credentials, try again."
        return render_template("login.html", error=error)


    return render_template("login.html")

@app.route('/loggedout/',methods=["GET","POST"])
def loggedout():
    session['logged_in']=False
    session['invalid']=False
    session.pop('username','password')
    return render_template("index.html")

@app.route('/signup/')
def signup():
    form = RegistrationForm(request.form)
    return  render_template("signup.html",form=form)




@app.route('/signedup/',methods=["GET","POST"])
def signedup():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username = str(form.username.data)

            email = str(form.email.data)
            password = str(hash.sha256_crypt.encrypt((str(form.password.data))))
            Designation=str(form.Designation.data)
            PhNumber=str(form.PhNumber.data)
            c, conn = connection()



            x=c.execute("SELECT * FROM entries WHERE Username = '%s' " % (thwart(username)))


            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('signup.html', form=form)

            else:
                c.execute("INSERT INTO entries (Username,Password,Email,Designation,PhoneNumber) VALUES (%s, %s, %s, %s,%s);",
                          (thwart(username),thwart(password),thwart(email),thwart(Designation),thwart(PhNumber)
                           ))


                conn.commit()

                flash("Thanks for registering!")
                c.close()
                conn.close()


                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('outpatient'))

        return render_template("signup.html", form=form)

    except Exception as e:
        return (str(e))

@app.route('/outpatient/')
def outpatient():
    if session['logged_in']:
        return render_template("outpatient.html")
    if(not session['logged_in']):
        flash("You must log in to view this page")
        return redirect(url_for("login"))

@app.route('/outpatient/addpatient/')
def addpatient():
    return render_template("addpatient.html")


if __name__ == '__main__':
   app.run(debug=True)

