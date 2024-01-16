from extensions import db

courses = db.Table(
    'courses', 
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'))
)

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=True, unique=True)
    password = db.Column(db.String(20))
    students = db.relationship('Student', secondary=courses, lazy='subquery', backref=db.backref('teachers', lazy=True))

    def __repr__(self):
        return f'<Teacher {self.name}>'

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=True, unique=True)
    password = db.Column(db.String(20))

    def __repr__(self):
        return f'<Student {self.name}>'
