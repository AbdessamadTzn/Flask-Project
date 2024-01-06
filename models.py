from extensions import db

class_course = db.Table (
    "class_course", db.Model.metadata,
    db.Column("student_id", 
    db.Integer(), 
    db.ForeignKey("students.student_id")),
    db.Column("course_id", db.Integer(), db.ForeignKey("courses.course_id"))
)

'''
Use Single table inheritance (STI) for teachers and students
'''
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), nullable = False)
    lastName = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    person_type = db.Column(db.String(20))

    __mapper_args__ = {
        "polymorphic_identity": "person",
        "polymorphic_on": person_type
    }

    def __repr__(self):
        return "<{}: {} {}>".format(self.person_type, self.firstName, self.lastName)

class Student(Person):
    __tablename__ = "students"
    student_id = db.Column(db.Integer, primary_key=True)
    student_email = db.Column(db.String(50), db.ForeignKey("person.email"))
    course_id = db.relationship("Course", secondary=class_course, back_populates="courseStudents")
    __mapper_args__ = {
        "polymorphic_identity": "students",
    }

    def __repr__(self):
        return "<{}: {} {}>".format(self.student_id, self.firstName, self.lastName)

class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key = True)
    course_description = db.Column(db.String(100), nullable=False)
    courseStudents = db.relationship("Student", secondary=class_course, back_populates="course_id")
    teacher = db.relationship("Teacher", backref="taught_course")

    def __repr__(self):
        return "<{}: {}>".format(self.course_id, self.course_description)
    
class Teacher(Person):
    __tablename__ = "teachers"
    teacher_id = db.Column(db.Integer, primary_key = True)
    firstName  = db.Column(db.String(50), nullable = False)
    lastName  = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), db.ForeignKey("person.email"))
    taught_course = db.relationship("Course", backref="teacher", lazy="dynamic")
    __mapper_args__ = {
        "polymorphic_identity": "teachers",
    }

    def __repr__(self):
        return "<{}: {} {} {}>".format(self.firstName, self.lastName, self.taught_course)

