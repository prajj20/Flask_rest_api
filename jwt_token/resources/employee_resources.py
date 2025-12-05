from flask_restful import Resource
from flask import request
from models import Employee
from extensions import db
from flask_jwt_extended import jwt_required




class EmployeeList(Resource):
    @jwt_required()
    def get(self):
        employees = Employee.query.all()
        result = []
        for emp in employees:
            result.append({
                "id": emp.id,
                "name": emp.name,
                "email": emp.email,
                "salary": emp.salary
            })
        return result
    

    @jwt_required()
    def post(self):
        data = request.get_json()
        new_emp = Employee(
            name=data.get("name"),
            email=data.get("email"),
            salary=data.get("salary")
        )
        db.session.add(new_emp)
        db.session.commit()
        return {"message": "Employee added"}, 201
    


class EmployeeDetail(Resource):
    @jwt_required()
    def get(self, id):
        emp = Employee.query.get(id)
        if not emp:
            return {"error": "Employee not found"}, 404
        return {
            "id": emp.id,
            "name": emp.name,
            "email": emp.email,
            "salary": emp.salary
        }
    
    @jwt_required()
    def put(self, id):
        emp = Employee.query.get(id)
        if not emp:
            return {"error": "Employee not found"}, 404
        
        data = request.get_json()
        emp.name = data.get("name")
        emp.email = data.get("email")
        emp.salary = data.get("salary")

        db.session.commit()

        return {"message": "Employee updated"}
    
    @jwt_required()
    def delete(self, id):
        emp = Employee.query.get(id)
        if not emp:
            return {"error": "Employee not found"}, 404

        db.session.delete(emp)
        db.session.commit()
        return {"message": "Employee deleted"}