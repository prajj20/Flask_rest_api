from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///many_to_many.db"
db = SQLAlchemy(app)

# Association Table
student_course = db.Table('student_course',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    
    # Many-to-Many relationship
    courses = db.relationship('Course', secondary=student_course, backref='students')

# Course Model
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))


@app.route('/student', methods=['POST'])
def create_student():
    data = request.get_json()
    student = Student(name=data['name'])
    db.session.add(student)
    db.session.commit()
    return jsonify({"msg": "Student created", "id": student.id}), 201

@app.route('/course', methods=['POST'])
def create_course():
    data = request.get_json()
    course = Course(title=data['title'])
    db.session.add(course)
    db.session.commit()
    return jsonify({"msg": "Course created", "id": course.id}), 201


@app.route('/enroll', methods=['POST'])
def enroll_student():
    data = request.get_json()
    student = Student.query.get(data['student_id'])
    course = Course.query.get(data['course_id'])

    if not student or not course:
        return jsonify({"error": "Student or Course not found"}), 404

    student.courses.append(course)
    db.session.commit()

    return jsonify({"msg": f"Student {student.name} enrolled in {course.title}"}), 200
@app.route('/student/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({
        "id": student.id,
        "name": student.name,
        "courses": [{"id": c.id, "title": c.title} for c in student.courses]
    })
@app.route('/course/<int:id>', methods=['GET'])
def get_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    return jsonify({
        "id": course.id,
        "title": course.title,
        "students": [{"id": s.id, "name": s.name} for s in course.students]
    })


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)