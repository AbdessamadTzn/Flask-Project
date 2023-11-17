import os
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import re



app = Flask(__name__)

app.config['SECRET_KEY'] = 'teacherssecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///teacher.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
teacher_db = SQLAlchemy(app)
app.app_context().push()

class Teacher(teacher_db.Model):
    teacher_id = teacher_db.Column(teacher_db.Integer, primary_key=True)
    name = teacher_db.Column(teacher_db.String(20), nullable=False)
    email = teacher_db.Column(teacher_db.String(100), unique=True)
    password = teacher_db.Column(teacher_db.String(100))

    def __repr__(self):
        return '<Teacher %r>' % self.name

with app.app_context():
    teacher_db.create_all()


@app.route("/")
def index():
    return render_template('home.html')
@app.route("/login_sucess/<m>")
def log_suc(m):
    return render_template('profile.html', m=m)

@app.route("/", methods=['POST'])
def login():
    lmail = request.form['lmail']
    lpw = request.form['lpassword']
    #lrem = True if request.form['remember'] else False
    #Under improve & review...

    log = Teacher.query.filter_by(email=lmail, password=lpw).first()

    if not log:
        flash('Please check you login details and try again!')
        return render_template('home.html')
    else:
        return redirect(url_for('log_suc', m=log.name))
    

@app.route("/student")
def student():
    return render_template('studentlist.html')

@app.route("/signup_success/<name>")
def signup_success(name):
    return render_template('teachers.html', name=name)

@app.route("/t_signup", methods=['POST', 'GET'])  # sign up for teachers
def teacher():
    if request.method == 'POST':
        tname = request.form['tname']
        tmail = request.form['tmail']
        tpw = request.form['tpassword']
        tpwc = request.form['tpasswordconfirm']

        if not re.match(r"[a-zA-Z0-9._%+-]+@gmail+\.[a-zA-Z]{2,}", tmail):
            flash("Please enter a valid email address (e.g., test@gmail.com)")
            return render_template('signup.html')
        else:
            tuser = Teacher.query.filter_by(email=tmail).first()
            if tuser or tpw != tpwc:
                if tuser:
                    flash("Email address already exists, please login instead")
                if tpw != tpwc:
                    flash("You should re-enter the same password!")
                return render_template('signup.html')
            else:
                #TODO: hashing password
                new_tuser = Teacher(name=tname, email=tmail, password=tpw)

                try:
                    teacher_db.session.add(new_tuser)
                    teacher_db.session.commit()
                    return redirect(url_for('signup_success', name=tname))
                except Exception as e:
                    flash(f"Error signing up: {str(e)}")
                    return render_template('signup.html')

    return render_template('signup.html')


#Use it for checking perfermance of signing up...
@app.route("/teachers", methods=['GET'])
def get_teachers():
    teachers = Teacher.query.all()
    teacher_list = []
    for teacher in teachers:
        teacher_data = {
            'teacher_id': teacher.teacher_id,
            'email': teacher.email,
            'name': teacher.name,
            'password': teacher.password
        }
        teacher_list.append(teacher_data)

    return jsonify({'teachers': teacher_list})

if __name__ == '__main__':
    app.run(debug=True)
    