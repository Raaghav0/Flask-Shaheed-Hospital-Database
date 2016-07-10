from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash,get_flashed_messages
from contextlib import closing
import os
import MySQLdb
from MySQLdb import escape_string as thwart
app=Flask(__name__)
app.secret_key="ABCD123"    
from wtforms import Form , TextAreaField , PasswordField , validators
from passlib import hash
from xhtml2pdf import pisa
from cStringIO import StringIO

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

            email = str(form.email.data)
            username = str(form.username.data)
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

@app.route('/patientadd/',methods=['POST','GET'])
def patientadd():

    c,conn = connection()

    c.execute(
        "INSERT INTO outpatients (NAME,PARENT,EDUCATION,AGE,SEX, PLACE,PHONE, DINANK,TIMES, APM) VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s);",
        (thwart(request.form['usr']), thwart(request.form['parentname']), thwart(request.form['educat']),
         thwart(request.form['age']),
         thwart(request.form['o1']), thwart(request.form['address']), thwart(request.form['phno']),
                thwart(request.form['date']), thwart(request.form['time']), thwart(request.form['apm'])
         ))

    conn.commit()
    conn.close()
    c.close()
    flash("patient added to database")
    return redirect(url_for("outpatient"))

@app.route('/outpatient/viewpatient/')
def viewpatient():
    return render_template("viewpatient.html")
@app.route('/patientsearch/',methods=["GET","POST"])
def patientsearch():
    c,conn =connection()
    c.execute("SELECT * FROM outpatients WHERE NAME LIKE %s ", ("%" + request.form['pat'] + "%",))
    data=c.fetchall()
    return render_template("viewpatient.html",data=data)
@app.route('/printpatient/',methods=["POST"])
def printpatient():
    str1 =request.form['submit']
    str2 = ""
    for i in str1:
        if(i==" "):
            break
        str2=str2 + i
    id_toprint=int(str2)
    c, conn = connection()
    c.execute("SELECT * FROM outpatients WHERE ID = %d " %id_toprint)
    data_toprint=c.fetchall()
    i=data_toprint[0];
    return render_template("print_template.html",i=i)



if __name__ == '__main__':
   app.run(debug=True)
   session['logged_in']=False

