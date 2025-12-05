from flask import Flask ,request ,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    age = db.Column(db.Integer,nullable = False)
    course = db.Column(db.String(100), nullable=False)
# now create here restfull api resource of student List
class StudentListResource(Resource):
    def get(self):
        students = Student.query.all()
        result = []
        for s in students:
            result.append({
                "id":s.id,
                "name":s.name,
                "age":s.age,
                "course":s.course
            })
        return result , 200
    
    def post(self):
        data = request.get_json()
        s_id = data.get('id')
        s_name = data.get('name')
        s_age = data.get('age')
        s_course = data.get('course')
        new_student = Student(id=s_id,name=s_name,age=s_age,course=s_course)

        db.session.add(new_student)
        db.session.commit()

        return {
            "id":new_student.id,
            "name":new_student.name,
            "age":new_student.age,
            "course":new_student.course

        },201
# Resource for single student  get , put , delete
class StudentResource(Resource):
    def get(self,student_id):
        student = Student.query.get(student_id)
        if not student:
            return {
                  "error": f"Student with ID {student_id} not found"
            },404
        return {
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "course": student.course
        }, 200
    def put(self,student_id):
        student = Student.query.get(student_id)
        if not student:
             return {"error": "Student not found to update"}, 404
        data = request.get_json()
        # student.id = data.get('id')
        student.name = data.get('name')
        student.age = data.get('age')
        student.course = data.get('course')

        db.session.commit()

        return {
            "mag":"updated sucessfully",
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "course": student.course
        }, 200
    
    def delete(self,student_id):
        student = Student.query.get(student_id)
        if not student:
            return {"error": "Student not found to delete "}, 404
        
        db.session.delete(student)
        db.session.commit()

        return {"message": "Student deleted"}, 200






    






api.add_resource(StudentListResource,'/students')
api.add_resource(StudentResource,'/student/<int:student_id>')
with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)



