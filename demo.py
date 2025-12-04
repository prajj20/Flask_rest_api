from flask import Flask, request, url_for, jsonify, session, redirect
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
# from flask.ext.cors import CORS
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.secret_key = 'anurag'

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)


class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(30), unique= False, nullable= False)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "role": self.role
        }
    
def login_required(func):
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return {"error": "Unauthorized. Please login first"}, 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route("/", methods=["GET"])
def default_login_page():
    return {
        "message": "Welcome to Login Page",
        "instructions": "POST username & password to /login"
    }

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "Username and password required"}, 400

    if Users.query.filter_by(username=username).first():
        return {"error": "Username already taken"}, 400

    hashed_pw = generate_password_hash(password)

    new_user = Users(username=username, password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return {"message": "User registered successfully"}, 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = Users.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash, password):
        return {"error": "Invalid username or password"}, 401

    session["user_id"] = user.id


    return {"message": "Login successful", "user": username}, 200

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

class EmpResource(Resource):
    
    @login_required
    def get(self, emp_id=None):

        if emp_id is None:
            employees = Employees.query.all()
            return [e.to_dict() for e in employees], 200

        emp = Employees.query.get(emp_id)

        if emp:
            return emp.to_dict(), 200
    
        return {"error": "Employee not found"}, 404

    @login_required
    def post(self):
        new_emp = request.get_json()
        if "first_name" not in new_emp or "last_name" not in new_emp or 'age' not in new_emp or 'role' not in new_emp:
            return {"error":"fill first, last, age,role data properly"}, 400
        emp = Employees(
        
        first_name=new_emp["first_name"],
        last_name=new_emp["last_name"],
        age=new_emp["age"],
        role=new_emp["role"]    
    )
        db.session.add(emp)
        db.session.commit()

        return ({
          "message": "Employee created successfully",
          "item": request.get_json(emp)
        }), 201

    @login_required    
    def delete(self, emp_id=None):
        if emp_id is None:
            return {"error": "Pass employee id"}
        
        emp = Employees.query.get(emp_id)

        if emp:
            db.session.delete(emp)
            db.session.commit()
            return {'message':'Employee deleted successfully'}, 400
    
        return {"error": "Employee not found"}, 404

    @login_required   
    def put(self, emp_id=None):
        if emp_id is None:
            return {"error": "Provide employee id"}, 400
        
        emp = Employees.query.get(emp_id)
        if emp is None:
            return {"error": "Employee not found"}, 404

        data = request.get_json()
        emp.first_name = data.get("first_name", emp.first_name)
        emp.last_name = data.get("last_name", emp.last_name)
        emp.age = data.get("age", emp.age)
        emp.role = data.get("role", emp.role)

        db.session.commit()

        return {
            "message": "Employee updated successfully",
            "item": emp.to_dict()
        }, 200
    

api.add_resource(EmpResource, '/emp','/emp/<int:emp_id>')

if __name__ == '__main__':
    with app.app_context():  
        db.create_all()     
    app.run(debug=True, host="0.0.0.0")