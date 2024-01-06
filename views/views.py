from flask import Blueprint, render_template, jsonify
# from models import Teacher

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template("home.html")

# @views.route("/teachers_database", methods=['GET'])
# def get_teachers():
#     teachers = Teacher.query.all()
#     teacher_list = []
#     for teacher in teachers:
#         teacher_data = {
#             'teacher_id': teacher.teacher_id,
#             'email': teacher.email,
#             'name': teacher.name,
#             'Hashed Password': teacher.password
#         }
#         teacher_list.append(teacher_data)
        
#     return jsonify({'teachers': teacher_list})
