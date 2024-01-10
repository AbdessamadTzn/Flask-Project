from extensions import db

'''
A teacher will aadd students to list if teacher.course==student.student
->Assign course to student
->Assign course to teacher
->Teacher check absence of student: True or False
Teacher-Student: Many to Many using course table


'''

class Teacher(db.Model):
    __table__ == 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=True, unique = True)
    password = db.Column(db.String(20))


    def __repr__(self):
        return f'<Teachers: {self.name}>'

class Student(db.Model):
    __table__ == 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=True, unique = True)
    password = db.Column(db.String(20))

    def __repr__(self):
        return f'<Students: {self.name}>'