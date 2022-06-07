import mysql.connector
from flask import Flask, render_template, request, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, EmailField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask import session

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'SECRET'
Bootstrap(app)

db = mysql.connector.connect(host="localhost",
user="root", password="Ishanvi@18", database="abhi")
mycursor = db.cursor()

# query="""use abhi;
# SHOW TABLES"""
# x=mycursor.execute(query,multi=True)
# for i in list(x):
#     y=list(i)
#     if ('users',) not in y:
#         try:
#             query="""CREATE TABLE USERS(ID int,
#             name varchar(100),password varchar(100))"""
#             mycursor.execute(query)
#             print("success")

#         except:
#              print("unsuccessfull")
#     else:
#         print("already present")
#         pass
#     break

try:
    query = """CREATE TABLE USERS(ID int,
    name varchar(100),password varchar(100))"""
    mycursor.execute(query)
    print("success")
except:
    print("Already present")


@app.route("/",methods=['GET','POST'])
def home():
    if request.method=='POST':
        givenname = request.form['mygname']
        givenpassword = request.form['mygpassword']
        q="SELECT * FROM users WHERE name=%s AND password=%s"
        a=(givenname,givenpassword)
        mycursor.execute(q, a)
        record=mycursor.fetchone()
        if record:
            session['Loggedin']=True
            session['username']=givenname
            # flash("logged in successfully")
            return render_template("home.html",v=session.get('username'))

        else:
            flash("username or password did not match")
            return render_template("login.html")
    else:
       return render_template("login.html")         


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['myname']
        password = request.form['mypassword']
        repassword = request.form['myrepassword']

        if name=="" and password=="":
            flash("Please enter valid name and password")
            return render_template("register.html")

        else:
            if repassword == password and name!="" and password!="":
                # query=("""INSERT INTO users('name','password') VALUES(%s,%s)"""%(name,password))
                s = "INSERT INTO users (name, password) VALUES (%s, %s)"
                t = (name, password)
                mycursor.execute(s, t)

                db.commit()
                flash("Registered successfully")

            else:
                flash("Password does not match")    

    # return redirect('/')
    return render_template("register.html")

if __name__=='__main__':
    app.run(debug=True)