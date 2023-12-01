from flask import Blueprint, render_template, request, flash, redirect, url_for
import re
from passlib.hash import pbkdf2_sha256

authTeachers = Blueprint('auth', __name__)
from models import Teacher
from extensions import db


@authTeachers.route("/teachers/login_sucess/<teacherName>")
def teacher_login_success(teacherName):
    return render_template('profile.html', teacherName=teacherName)

@authTeachers.route("/", methods=['POST'])
def login():
    teacher_log_mail = request.form['teacher_log_mail']
    teacher_log_password = request.form['teacher_log_password']
    #lrem = True if request.form['remember'] else False
    #Under improve & review...

    log = Teacher.query.filter_by(email=teacher_log_mail, password=teacher_log_password).first()

    if not log:
        flash('Please check you login details and try again!')
        return render_template('home.html')
    else:
        return redirect(url_for('auth.teacher_login_success', teacherName=log.name))
    
@authTeachers.route("/student")
def student():
    return render_template('studentlist.html')

@authTeachers.route("/signup_success/<name>")
def signup_success(name):
    return render_template('teachers.html', name=name)

@authTeachers.route("/teacher/signup", methods=['POST', 'GET'])  # sign up for teachers
def teacher_signup():
    if request.method == 'POST':
        teacherName = request.form['tname']
        teacherMail = request.form['tmail']
        teacherPassword = request.form['tpassword']
        teacherPasswordConfirm = request.form['tpasswordconfirm']

        if not re.match(r"[a-zA-Z0-9._%+-]+@gmail+\.[a-zA-Z]{2,}", teacherMail):
            flash("Please enter a valid email address (e.g., test@gmail.com)")
            return render_template('signup.html')
        else:
            teacherExist = Teacher.query.filter_by(email=teacherMail).first()
            if teacherExist or teacherPassword != teacherPasswordConfirm:
                if teacherExist:
                    flash("Email address already exists, please login instead")
                if teacherPassword != teacherPasswordConfirm:
                    flash("You should re-enter the same password!")
                return render_template('signup.html')
            else:
                teacher_hashed_password = pbkdf2_sha256.hash(teacherPassword)
                new_tuser = Teacher(name=teacherName, email=teacherMail, password=teacher_hashed_password)

                try:
                    db.session.add(new_tuser)
                    db.session.commit()
                    return redirect(url_for('auth.signup_success', name=teacherName))
                except Exception as e:
                    flash(f"Error signing up: {str(e)}")
                    return render_template('signup.html')

    return render_template('signup.html')


