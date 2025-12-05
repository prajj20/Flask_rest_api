from extensions import db
from passlib.hash import pbkdf2_sha256 as sha256



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


    def generate_hash(password):
        return sha256.hash(password)
    
    def verify_hash(password, hashed):
        return sha256.verify(password, hashed)
    
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(70), unique=True)
    salary = db.Column(db.Integer)