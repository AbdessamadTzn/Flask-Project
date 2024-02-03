from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import re
from passlib.hash import pbkdf2_sha256

from models import Teacher, Student
from extensions import db

authTeachers = Blueprint('authTeacher', __name__)


@authTeachers.route("/teachers/login_success/<teacherName>")
def teacher_login_success(teacherName):
    return render_template('teachers/home.html', teacherName=teacherName)

@authTeachers.route("/teachers/studentsList", methods=['POST', 'GET'])
def studentsList():
    students = Student.query.all()
    return render_template('teachers/students_list.html', students=students)

@authTeachers.route("/", methods=['POST'])
def login():
    teacher_log_mail = request.form['teacher_log_mail']
    teacher_log_password = request.form['teacher_log_password']

    try:
        teacherLogin = Teacher.query.filter_by(email=teacher_log_mail).first()
    except Exception as e:
        print(f"Query Teacher's mail error: {str(e)}")

    if teacherLogin:
        if pbkdf2_sha256.verify(teacher_log_password, teacherLogin.password):
            return redirect(url_for('authTeacher.teacher_login_success', teacherName=teacherLogin.name))
        else:
            flash("Your password is incorrect!")
            return render_template('home.html')
    else:
        flash('Your email is isncorrect!')
        return render_template('home.html')

@authTeachers.route('teachers/add_student', methods=['GET', 'POST'])
def add_student():
    #TODO: Handle studentExist = Student.query.filter_by(id=id).first()

    if request.method == 'POST':
        studentName = request.form['student_name']
        studentEmail = studentName + '@schoolname.com'
        
        passwordString = f'{studentName}#schoolname'
        studentPassword = pbkdf2_sha256.hash(passwordString)
        new_student = Student(name=studentName, email=studentEmail, password=studentPassword)
        try:
            db.session.add(new_student)
            db.session.commit()
            flash('You have successfully add a student!', 'success')
            return render_template('teachers/students_list.html', studentName = studentName)
        except Exception as e:
            flash(f"Error adding student: {str(e)}")
            return render_template('teachers/add_student.html')
    return render_template('teachers/add_student.html')
@authTeachers.route('/teacher/students_list')
def get_students_list():
    return render_template('teachers/students_list.html')
# @authTeachers.route("/student")
# def student():
#     return render_template('studentlist.html')

@authTeachers.route("/signup_success/<name>")
def signup_success(name):
    return render_template('<h2>HI {name}, you can login now', name=name)

@authTeachers.route("/teacher/signup", methods=['POST', 'GET'])  # sign up for teachers
def teacher_signup():
    if request.method == 'POST':
        teacherName = request.form['tname']
        teacherMail = request.form['tmail']
        teacherPassword = request.form['tpassword']
        teacherPasswordConfirm = request.form['tpasswordconfirm']

        if not re.match(r"[a-zA-Z0-9._%+-]+@gmail+\.[a-zA-Z]{2,}", teacherMail):
            flash("Please enter a valid email address (e.g., test@gmail.com)")
            return render_template('teachers/signup.html')
        else:
            teacherExist = Teacher.query.filter_by(email=teacherMail).first()
            if teacherExist or teacherPassword != teacherPasswordConfirm:
                if teacherExist:
                    flash("Email address already exists, please login instead")
                if teacherPassword != teacherPasswordConfirm:
                    flash("You should re-enter the same password!")
                return render_template('teachers/signup.html')
            else:
                teacher_hashed_password = pbkdf2_sha256.hash(teacherPassword)
                new_tuser = Teacher(name=teacherName, email=teacherMail, password=teacher_hashed_password)

                try:
                    db.session.add(new_tuser)
                    db.session.commit()
                    flash('You have successfully signed up! Please log in.', 'success')
                    return render_template('home.html')
                except Exception as e:
                    flash(f"Error signing up: {str(e)}")
                    return render_template('teachers/signup.html')

    return render_template('teachers/signup.html')
# @authTeachers.route('/teachers/student_list/<teacherName>', methods=['GET'])
# def get_students(teacherName):
#     students = Student.query.all()
#     return render_template('teachers/students_list.html', teacherName=teacherName, students=students)