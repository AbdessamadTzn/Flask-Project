import os
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import re


db=SQLAlchemy()
DB_NAME = "teachers.db"

app = Flask(__name__)

app.config['SECRET_KEY'] = 'DJODNCWOICNWOIEACJOIEWJ'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from views.views import views
from auth.teachersRoutes import authTeachers


app.register_blueprint(views, url_prefix='/')
app.register_blueprint(authTeachers, url_prefix='/')



# with app.app_context():
#     teacher_db.create_all()









#Use it for checking perfermance of signing up...



if __name__ == '__main__':
    app.run(debug=True)
    