from flask_restful import Resource
from flask import request
from models import User
from extensions import db
from flask_jwt_extended import create_access_token

class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if User.query.filter_by(username=username).first():
            return {"error": "User already exists"}, 400
        
        new_user = User(
            username=username,
            password=User.generate_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully"}, 201
    


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()
        if not user or not User.verify_hash(password, user.password):
            return {"error": "Invalid username or password"}, 401
        
        access_token = create_access_token(identity=str(user.id))

        return {
            "message": "Login successful",
            "access_token": access_token
        }, 200