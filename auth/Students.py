from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import re
from passlib.hash import pbkdf2_sha256

authStudents = Blueprint('authStudent', __name__)

@authStudents.route('/students/home')
def student():
    return render_template('students/home.html')