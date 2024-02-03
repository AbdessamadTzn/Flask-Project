from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import re
from passlib.hash import pbkdf2_sha256
from models import Teacher
from extensions import db

authStudents = Blueprint('authStudent', __name__)

@authStudents.route('/students/home', methods=['POST', 'GET'])
def student():
    if request.method == 'POST':
        student_log_mail = request.form['student_log_mail']
        student_log_password = request.form['student_log_password']

        try:
            studentLogin = Student.query.filter_by(email=student_log_mail).first()
        except Exception as e:
            print(f"Error, query student's mail {str(e)}")
        
        if studentLogin:
            if pbkdf2_sha256(student_log_password, studentLogin.student_log_password):
                return render_template('home.html')
            else:
                pass
        else:
            flash("This email doesn't exist!")
            return render_template('students/home.html')


    return render_template('students/home.html')

