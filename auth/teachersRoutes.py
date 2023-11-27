from flask import Blueprint, render_template, request

authTeachers = Blueprint('auth', __name__)


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
        return redirect(url_for('teacher_login_success', teacherName=log.name))
    
@authTeachers.route("/student")
def student():
    return render_template('studentlist.html')

@authTeachers.route("/signup_success/<name>")
def signup_success(name):
    return render_template('teachers.html', name=name)

@authTeachers.route("/teacher/signup", methods=['POST', 'GET'])  # sign up for teachers
def teacher_signup():
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
@authTeachers.route("/teachers", methods=['GET'])
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

