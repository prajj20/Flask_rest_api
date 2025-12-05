from flask import Flask
from flask_restful import Api
from extensions import db, jwt
from resources.user_resources import UserRegister, UserLogin
from resources.employee_resources import EmployeeList, EmployeeDetail

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///emp_jwt.db"
app.config["JWT_SECRET_KEY"] = "secret-123"

db.init_app(app)
jwt.init_app(app)
api = Api(app)


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(EmployeeList, "/employees")
api.add_resource(EmployeeDetail, "/employees/<int:id>")


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)