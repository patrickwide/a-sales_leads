from flask import Flask,render_template,request,redirect,session,jsonify,json
import pymysql
import re
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "ssfks6787"#just a rundom string of characters.


UPLOAD_FOLDER = "static/img"
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif','svg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/school_home', methods=['POST', 'GET'])
def school_home():
    return render_template("school_home.html")

#teachers part start here
@app.route('/teacher_home', methods=['POST', 'GET'])
def teacher_home():
    return render_template("teacher_home.html")

@app.route('/my_classes', methods=['POST', 'GET'])
def my_classes():
    return render_template("my_classes.html")


@app.route('/my_students', methods=['POST', 'GET'])
def my_students():
    return render_template("my_students.html")

#teachers part end here


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index.html")


#route for the school and students to join
@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template("register.html")
#school join app start here----------------------------------------------------


#actual route to send data to the database----------------------

@app.route("/join_app",methods =['POST','GET'])
def join_app():
    if request.method == "POST":
        school_name = request.form['school_name']
        school_type = request.form['school_type']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        if school_name == "" or email == "" or school_type == "" or phone == "" or password == "":
            return render_template("register.html")

        else:
            conn = makeConnection()
            cur = conn.cursor()
            sql = "INSERT INTO `schools`(`school_name`, `type`, `school_email`, `school_phone`, `school_password`) VALUES (%s,%s,%s,%s,%s)"
            cur.execute(sql, (school_name,school_type,email,phone,password))
            conn.commit()

            conn_1 = makeConnection()
            cur_1 = conn_1.cursor()
            sql_1 = "SELECT * FROM schools WHERE school_email=%s AND school_password=%s"
            cur_1.execute(sql_1, (email, password))

            if cur_1.rowcount >= 1:
                results = cur_1.fetchall()
                session["database_name"] = results[0][0]
                db = session["database_name"]
                db_1 = f"school_{db}_1"

                conn_2 = pymysql.connect("localhost", "root")
                cursor_2 = conn_2.cursor()

                cursor_2.execute(f"CREATE DATABASE {db_1}")
                cursor_2.execute(
                    f"CREATE TABLE {db_1}.`classes` ( `id` INT NOT NULL AUTO_INCREMENT ,  `grade_form` VARCHAR(100) NOT NULL ,    PRIMARY KEY  (`id`)) ENGINE = InnoDB;")
                cursor_2.execute(
                    f"CREATE TABLE {db_1}.`subjects` ( `id` INT NOT NULL AUTO_INCREMENT , `subject_name` VARCHAR(100) NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;")
                cursor_2.execute(
                    f"CREATE TABLE {db_1}.`teachers` ( `id` INT NOT NULL AUTO_INCREMENT ,  `f_name` TEXT NOT NULL ,  `l_name` TEXT NOT NULL ,  `email` VARCHAR(50) NOT NULL ,  `phone` INT(20) NOT NULL ,  `gender` TEXT NOT NULL ,  `grade_name` VARCHAR(50) NOT NULL ,  `subject_course` VARCHAR(50) NOT NULL ,  `password` VARCHAR(100) NOT NULL ,    PRIMARY KEY  (`id`)) ENGINE = InnoDB;")
                cursor_2.execute(
                    f"CREATE TABLE {db_1}.`students` ( `id` INT NOT NULL AUTO_INCREMENT ,  `adm_num` VARCHAR(100) NOT NULL ,  `f_name` TEXT NOT NULL ,  `l_name` TEXT NOT NULL ,  `class_grade` VARCHAR(50) NOT NULL ,  `p_name` TEXT NOT NULL ,  `phone` INT(20) NOT NULL ,  `email` VARCHAR(50) NOT NULL ,  `password` VARCHAR(50) NOT NULL ,    PRIMARY KEY  (`id`)) ENGINE = InnoDB;")
                cursor_2.execute(
                    f"CREATE TABLE {db_1}.`assessments` ( `id` INT NOT NULL AUTO_INCREMENT ,  `assessment_name` VARCHAR(100) NOT NULL ,  `date` DATE NOT NULL DEFAULT CURRENT_TIMESTAMP ,  `type` INT(50) NOT NULL ,  `creater` INT(50) NOT NULL ,  `file` VARCHAR(50) NOT NULL ,  `class` INT(50) NOT NULL ,  `total` INT(50) NOT NULL ,    PRIMARY KEY  (`id`)) ENGINE = InnoDB;")
                cursor_2.execute(
                    f"CREATE TABLE {db_1}.`marks` ( `id` INT NOT NULL AUTO_INCREMENT ,  `std_id` INT(50) NOT NULL ,  `class_id` INT(50) NOT NULL ,  `teacher_id` INT(50) NOT NULL ,  `assessment_id` INT(50) NOT NULL ,    PRIMARY KEY  (`id`)) ENGINE = InnoDB;")
                cursor_2.execute(
                    f"CREATE TABLE {db_1}.`gallary` ( `id` INT NOT NULL AUTO_INCREMENT ,  `image` VARCHAR(100) NOT NULL ,  `posted_by` VARCHAR(100) NOT NULL ,  `posted_on` VARCHAR(100) NOT NULL DEFAULT CURRENT_TIMESTAMP ,    PRIMARY KEY  (`id`)) ENGINE = InnoDB;")
                conn_2.commit()

                return f"database {db} created"
            else:
                return "hello am not there"

#school join app end here----------------------------------------------------school join app end here
#login stars here------------------------------------------------------------------

@app.route('/login', methods=['POST', 'GET'])
def login():#this will check from schools table and the teachers and students
        return render_template("login.html")


@app.route('/log_in', methods=['POST', 'GET'])
def log_in():
    if request.method == "POST":
        email_phone = request.form['email_phone']
        password = request.form['password']
        email_run = forEmail()
        phone_run = forPhone()

        if email_phone == "" or password == "":
            return render_template("login.html")

        elif len(re.findall("[\w._%+-]{2,20}@[\w.-]{2,20}.[A-Za-z]{2,3}", email_phone)):
            return email_run

        elif len(re.findall("[0-9]{10,11}", email_phone)):
            return phone_run
        else:
            msg = "please check your phone/email"
            return render_template("login.html", msg1=msg)
    else:
        return render_template("login.html")



def forEmail():
    if request.method == "POST":
        school_email = str(request.form["email_phone"])
        password = str(request.form["password"])
        if school_email == "" or password == "":
            return render_template("login.html")
        else:
            conn = makeConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM schools WHERE school_email=%s AND 	school_password=%s"
            cur.execute(sql, (school_email, password))
            if cur.rowcount >= 1:  # if this evaluates to true..
                # ...then we login the user by creating a sesssion.
                results = cur.fetchall()
                session['db'] = results[0][0]
                a = session['db']
                print(a)

                session['school_email'] = school_email
                return "connected"#redirect('/home')
            else:
                return render_template("login.html", msg="The Email/Password Combination is Incorrect!")
    else:
        return render_template("login.html", msg="Wrong Request Method")


def forPhone():
    if request.method == "POST":
        school_phone = str(request.form["email_phone"])
        password = str(request.form["password"])
        if school_phone == "" or password == "":
            return render_template("login.html")
        else:
            conn = makeConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM schools WHERE school_phone=%s AND 	school_password=%s"
            cur.execute(sql, (school_phone, password))
            if cur.rowcount >= 1:  # if this evaluates to true..
                # ...then we login the user by creating a sesssion.
                results = cur.fetchall()
                session['db'] = results[0][0]
                a = session['db']

                session['school_email'] = school_phone
                return "connected"#redirect('/home')
            else:
                return render_template("login.html", msg="The Email/Password Combination is Incorrect!")
    else:
        return render_template("login.html", msg="Wrong Request Method")


#login ends here------------------------------------------------------------------



#second location starts here----------------------------------------------------second form starts here
@app.route('/location', methods=['POST', 'GET'])
def location():
    if 'school_email' in session:

        return render_template("location_set.html")
    else:
        return render_template('location_set.html',msg="Please Login First")


@app.route('/locations_dit', methods=['POST', 'GET'])
def second_form():
    if 'school_email' in session:
        wizard_picture = str(request.form["wizard"])
        location_1 = str(request.form["location_1"])
        location_2 = str(request.form["location_2"])
        location_3 = str(request.form["location_3"])
        facebook = str(request.form["facebook"])
        instagram = str(request.form["instagram"])
        twitter = str(request.form["twitter"])
        youtube = str(request.form["youtube"])
        if wizard_picture == "" or location_1 == "" or location_2 == "" or location_3 == "":
            msgA = f"error"
            msgB = f"You clicked the button, problem encountered!"
            msgC = f"error"
            msgD = f"Next"
            return jsonify({"success": True,"msgA": msgA,"msgB": msgB,"msgC": msgC,"msgD": msgD})
        else:
            conn = makeConnection()
            cur = conn.cursor()
            id = session['db']

            sql = "UPDATE schools SET school_logo=%s,location_1=%s,location_2=%s,location_3=%s,facebook=%s,instagram=%s,twitter=%s,youtube=%s WHERE id=%s"
            cur.execute(sql, (wizard_picture,location_1,location_2,location_3,facebook,instagram,twitter,youtube,id))
            conn.commit()

            insert = request.form["insert"]
            insert = insert.split(",")
            a = session['db']

            conn = pymysql.connect("localhost", "root", "", f"school_{a}_1")
            cur = conn.cursor()

            for subjects in insert:
                sql = ("INSERT INTO `subjects`(`subject_name`) VALUES (%s)")
                cur.execute(sql, (subjects))
                a = "SELECT id FROM `subjects` WHERE 1"
                a = cur.execute(a)
                b = "ALTER TABLE `marks`  ADD `%s` INT(50) NOT NULL  AFTER `assessment_id`;"
                cur.execute(b,(a))
                c = f"ALTER TABLE `classes`  ADD `%s` INT(50) NOT NULL  AFTER `grade_form`;"
                cur.execute(c,(a))

                conn.commit()

            b = "ALTER TABLE `marks`  ADD `total` INT(50) NOT NULL  AFTER `assessment_id`;"
            cur.execute(b)
            conn.commit()

            msgA = f"success"
            msgB = f"You clicked the button successfully!"
            msgC = f"success"
            msgD = f"Next"
            return jsonify({"success": True,"msgA": msgA,"msgB": msgB,"msgC": msgC,"msgD": msgD})

    else:
        return render_template('login.html',msg="Please Login First")


#second add_class starts here----------------------------------------------------second form starts here
@app.route('/add_class', methods=['POST', 'GET'])
def add_class():
    return render_template("add_class.html")

@app.route('/add_class_first', methods=['POST', 'GET'])
def add_class_first():
    grade = str(request.form["grade"])
    grade_name = str(request.form["grade_name"])
    if grade == "Choose ..." or len(grade_name) <= 0:
        msg = "an error ..."
        types = "error"
        return jsonify({"success": True, "msg": msg, "types": types})
    else:
        grade_form = f"{grade} {grade_name}"
        a = session['db']
        conn = pymysql.connect("localhost", "root", "", f"school_{a}_1")
        cur = conn.cursor()
        sql = ("INSERT INTO `classes`(`grade_form`) VALUES (%s)")
        cur.execute(sql, (grade_form))
        conn.commit()
        msg = f"successfully added"
        types = "success"
        return jsonify({"success": True, "msg": msg, "types": types})

@app.route('/attendance_form', methods=['POST', 'GET'])
def attendance_form():
    return render_template("attendance_form.html")

#second add_class ends here----------------------------------------------------second form starts here


#add_teacher_table form starts here----------------------------------------------------second form ends here

@app.route('/add_teacher_table', methods=['POST', 'GET'])
def add_teacher_table():
    return render_template("add_teachers_table.html")#"""we wil use thesame  tables to add techers and students  """

@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    first_name = str(request.form["first_name"])
    last_name = str(request.form["last_name"])
    email = str(request.form['email'])
    phone = str(request.form['phone'])
    gender = str(request.form['gender'])
    grade_form = str(request.form['class_name'])
    subject = str(request.form['subject'])
    pass_code = str("police911")
    if len(first_name) <= 2 or len(last_name)  <= 2 or len(email) <= 2 or len(phone) <= 2 or len(gender) == 0 or len(grade_form) == 0 or len(subject) == 0:
        msg = "please fill all the spaces"
        types = "error"
        return jsonify({"success": True,"msg":msg,"types":types})
    else:

        a = session['db']
        conn = pymysql.connect("localhost", "root", "", f"school_{a}_1")
        cur = conn.cursor()
        sql = "INSERT INTO `teachers`(`f_name`, `l_name`, `email`, `phone`, `gender`, `grade_name`, `subject_course`, `password`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
        cur.execute(sql,(first_name,last_name,email,phone,gender,grade_form,subject,pass_code))

        my_id = str("1")
        subjects = ("SELECT `id`FROM `subjects` WHERE `subject_name`=%s")
        cur.execute(subjects,(subject))
        subjects = cur.fetchall()
        subjects = str(subjects[0][0])
        subjects = int(subjects)
        update = "UPDATE `classes` SET `%s`=%s WHERE `grade_form`=%s"
        cur.execute(update,(subjects,my_id,grade_form))
        conn.commit()

        msg = f"added"
        types = "success"
        return jsonify({"success": True,"msg":msg,"types":types})

#add_teacher_table form ends here----------------------------------------------------second form ends here
a = 'SELECT `id`FROM `subjects` WHERE `subject_name` = "mathematics"'
b = 'UPDATE `classes` SET `8`="4" WHERE `grade_form` = "2 west"'
#add_student_table form starts here----------------------------------------------------second form ends here
@app.route('/add_student_table', methods=['POST', 'GET'])
def add_student_table():
    return render_template("add_student.html")

@app.route('/add_student', methods=['POST'])
def add_student():
    s_a_num = request.form["s_a_num"]
    s_f_name = request.form["s_f_name"]
    S_l_name = request.form['S_l_name']
    s_grade = request.form['s_grade']
    p_name = request.form['p_name']
    p_phone = request.form['p_phone']
    p_email = request.form['p_email']
    pass_code = "police911"

    if len(s_a_num) <= 2 or len(s_f_name)  <= 2 or len(S_l_name) <= 2 or len(s_grade) == 0 or len(p_name) <= 2 or len(p_phone) < 10 or len(p_email) <= 2:
        msg = "please fill all the spaces"
        types = "error"
        return jsonify({"success": True,"msg":msg,"types":types})
    else:
        msg = "added"
        types = "success"
        return jsonify({"success": True, "msg": msg, "types": types})

#add_student_table form ends here----------------------------------------------------second form ends here

#assessments page starts here---------------------------------------------------------------------------------
@app.route('/assessments', methods=['POST', 'GET'])
def assessments():
    return render_template("assessments.html")

@app.route('/new_assessment', methods=['POST', 'GET'])
def new_assessment():
    if request.method == "POST":
        new_assessment = str(request.form["new_assessment"])
        return redirect('/add_pdf')
    else:
        return "hello world"
#assessments page ends here---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------

@app.route('/take', methods=['POST'])
def take():
    name = request.form["name"]
    if name == "":
        return jsonify({"success": True,"name":"none"})
    else:
        return jsonify({"success": True,"name":name})




@app.route('/add_pdf', methods=['POST', 'GET'])
def addPdf():
    return render_template("add_pdf.html")


@app.route('/assessment', methods=['POST', 'GET'])
def assessment():
    return render_template("assessment_marks.html")


@app.route('/try', methods=['POST', 'GET'])
def try_page():
    return render_template("try.html")




#route for the teacher and students to join
@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
        return render_template("sign_up.html")




@app.route('/add_class_form', methods=['POST', 'GET'])
def add_class_form():
    if request.method == "POST":
        grade = request.form['grade']
        grade_name = request.form['grade_name']

        return f"{grade},{grade_name}"
    else:
        return "hello 2"

@app.route('/school_read', methods=['POST', 'GET'])
def school_read():
    return render_template("school_read.html")

@app.route('/school_assessment_files', methods=['POST', 'GET'])
def school_assessment_files():
    return render_template("school_assessment_files.html")



@app.route('/school_settings', methods=['POST', 'GET'])
def school_settings():
    return render_template("school_settings.html")


@app.route('/gallery', methods=['POST', 'GET'])
def gallery():
    return render_template("gallery.html")


@app.route('/send_massage', methods=['POST', 'GET'])
def send_massage():
    return render_template("send_massage.html")


@app.route('/calender', methods=['POST', 'GET'])
def calender():
    return render_template("calender.html")



@app.route("/info",methods=['POST','GET'])
def info():
    if request.method == "POST":
        username = str(request.form['Name'])

        return render_template("try.html", msg=username)

@app.route('/logout',methods=['POST','GET'])
def logout():
    session.pop('school_email',None)
    return redirect('/')


def makeConnection():
    host = "127.0.0.1"
    user = "root"
    password = ""
    database = "grading_app" #this is the name of your database
    return pymysql.connect(host,user,password,database)



if __name__ == "__main__":
    app.run(debug=True, port=4200)
