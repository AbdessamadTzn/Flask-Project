import os
from flask import Flask, render_template, jsonify
import psycopg2
from dotenv import load_dotenv
from extensions import db
from models import Teacher, Student


app = Flask(__name__)

app.config['SECRET_KEY'] = 'DJODNCWOICNWOIEACJOIEWJ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'db', 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from auth.Teachers import authTeachers

app.register_blueprint(authTeachers, url_prefix='/')

@app.route('/')
def index():
    return render_template('home.html')
@app.route('/Teachers')
def get_students():
    students = Teacher.query.all()
    student_list = []
    for student in students:
        student_data = {
            'student_id': student.id,
            'email': student.email,
            'name': student.name,
            'Hashed Password': student.password
        }
        student_list.append(student_data)

    return jsonify({'teachers': student_list})



if __name__ == '__main__':
    # Create the 'db' directory if it doesn't exist
    db_dir = os.path.join(os.getcwd(), 'db')
    os.makedirs(db_dir, exist_ok=True)

    # Create the database tables
    with app.app_context():
        db.create_all()

    # Run the Flask application
    app.run(debug=True)