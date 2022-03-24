from flask import Flask,render_template,request,redirect,session,jsonify,json`
# import pymysql
import re
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os



app = Flask(__name__)
app.secret_key = "ssfks6787"#just a rundom string of characters.


@app.route('/new', methods=['POST', 'GET'])
def new():
    return render_template("new.html")


@app.route('/new2', methods=['POST', 'GET'])
def new2():
    return render_template("new2.html")

@app.route('/new3', methods=['POST', 'GET'])
def new3():
    return render_template("new3.html")



#adding the routes
@app.route('/', methods=['POST', 'GET'])
def index():
    if "username" not in session:
        return redirect('/accounts')
    else:
        user = session["username"]
        date_today = "2021-06-17"

        conn = makeConnection()
        cur = conn.cursor()
        sql = "SELECT * FROM `contacts` WHERE user=%s ORDER BY id DESC"
        cur.execute(sql,(user))

        conn1 = makeConnection()
        cur1 = conn1.cursor()
        sql1 = "SELECT * FROM `contacts` WHERE user=%s AND date_to_call=%s ORDER BY id DESC"
        cur1.execute(sql1,(user,date_today))

        if cur.rowcount >= 1:
            if cur1.rowcount < 1:
                style = "fa-info-circle"
                msg = "No notifications"
                return render_template('index.html', result=cur.fetchall(),msg=msg,style=style)
            else:
                count = cur1.rowcount
                return render_template('index.html', result=cur.fetchall(),resulted=cur1.fetchall(),count=count)
        else:
            return render_template("index.html")


@app.route('/accounts', methods=['POST', 'GET'])
def accounts():
    return render_template("accounts.html",text="Sign in with your credentials")

@app.route('/add_contacts',methods=['POST','GET'])
def add_contacts():
    if 'username' not in session:
        return render_template('accounts.html')

    else:

        if request.method == "POST":
            phone = str(request.form['phone'])
            name = str(request.form['name'])
            date_to_call = str(request.form['date_to_call'])
            posted_on_date = str("6-16-2021")
            package = str(request.form['package'])
            area = str(request.form['area'])
            more = str(request.form['more'])
            user = session['username']

            if phone == "" or name == "" or date_to_call == "" or posted_on_date == "" or package == "" or area == "":
                all = "done"
            elif more == "":
                more = "N/A"

            conn = makeConnection()
            cur = conn.cursor()
            sql = "INSERT INTO `contacts`(`phone`, `name`, `date_to_call`, `package`, `area`, `more`, `posted_on_date`, `user`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql, (phone, name, date_to_call,package,area,more,posted_on_date,user))
            conn.commit()

            style_success = "fa-check-square"
            msg_success = "Successfully added"

            return redirect('/')

        else:
            return redirect('/')


@app.route('/sign-in',methods=['POST','GET'])
def sign_in():
    if "username" not in session:

        if request.method == "POST":

            username_email = str(request.form['username_email'])
            password = str(request.form['password'])
            if username_email == "" or password == "":
                msg = "please fill all the fields"
                return render_template('accounts.html',msg=msg)
            else:
                conn = makeConnection()
                cur = conn.cursor()

                conn1 = makeConnection()
                cur1 = conn1.cursor()


                check_username = "SELECT * FROM users WHERE username = %s"
                check_email = "SELECT * FROM users WHERE email = %s"

                cur.execute(check_username, (username_email))
                cur1.execute(check_email, (username_email))

                if cur.rowcount >= 1 or cur1.rowcount >= 1:
                    results = cur.fetchall() or cur1.fetchall()
                    session['username'] = results[0][0]
                    return redirect('/')
                else:
                    return render_template("accounts.html",text="invalid info!")


        return redirect('/')
    else:
        return redirect('/')




@app.route('/delete', methods=['POST','GET'])
def delete():
    if request.method == "POST":
        id = str(request.form["contact_id"])
        user = str(request.form["user_id"])
        if id == "" or user == "":
            return "redirect("")"
        else:
            conn = makeConnection()
            cur = conn.cursor()
            sql = "DELETE FROM contacts WHERE id=%s AND user=%s"
            cur.execute(sql, (id,user))
            conn.commit()
            return redirect("/")
    else:
        return "redirect("")"



@app.route("/update", methods=['POST','GET'])
def update():
    if request.method == "POST":
        id = str(request.form['id'])
        phone = str(request.form['phone'])
        name = str(request.form['name'])
        package = str(request.form['package'])
        area = str(request.form['area'])
        more = str(request.form['more'])
        user = session['username']
        date_to_call = str(request.form['date_to_call'])

        if phone == "" or name == "" or package == "" or area == "" or date_to_call == "":
            msg = "fill all ""*"" fields"
            return redirect("/")

        else:
            conn = makeConnection()
            cur = conn.cursor()
            sql = "UPDATE contacts SET phone=%s,name=%s,date_to_call=%s,package=%s,area=%s,more=%s,user=%s WHERE id=%s"
            cur.execute(sql, (phone, name, date_to_call, package, area, more, user,id))
            conn.commit()
            return redirect('/')
    else:
        return redirect("/")


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if "username" in session:
        session.pop('username')
        return redirect("/accounts")
    else:
        return redirect('/accounts')


@app.route('/sign-up', methods=['POST','GET'])
def sign_up():
    if request.method == "POST":
        username = str(request.form['username'])
        email = str(request.form['email'])
        password = str(request.form['password'])
        if email == "" or username == "" or password == "":
            msg = "please fill all the fields"
            return "blank"
        else:
            conn = makeConnection()
            cur = conn.cursor()
            check_username = "SELECT username FROM users WHERE username = %s"
            check_email = "SELECT email FROM users WHERE email = %s"
            cur.execute(check_username, (username))
            cur.execute(check_email, (email))

            if cur.rowcount >= 1:
                msg = f"Username already taken"
                return render_template("accounts.html",msg=msg)
            elif cur.rowcount >= 1:
                msg = f"Email already taken"
                return render_template("accounts.html" ,msg=msg)
            else:
                sql = "INSERT INTO users(username,email,password)values(%s,%s,%s)"
                cur.execute(sql, (username, email, password))
                conn.commit()
                msg = "User Added Successfully"
                return render_template('accounts.html',msg=msg)
    else:
        return redirect('/account')

def makeConnection():
    host = "127.0.0.1"
    user = "root"
    password = ""
    database = "sales_app"  # this is the name of your database
    return pymysql.connect(host, user, password, database)


    # return pymysql.connect("127.0.0.1","root","","login_example")

if __name__ == "__main__":
    app.run(debug=True, port=4790)
