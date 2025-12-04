from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///one-to-one.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    profile = db.relationship("Profile", backref="user", uselist=False)
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    city = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)
     
with app.app_context():
    db.create_all()

@app.route('/user', methods=['POST','GET'])
def create_user():
    data = request.get_json()
    user = User(username=data['username'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User Created", "id": user.id}), 201

@app.route('/profile', methods=['POST'])
def create_profile():
    data = request.get_json()
    user_id = data['user_id']

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.profile:
        return jsonify({"error": "User already has a profile"}), 400

    profile = Profile(
        age=data['age'],
        city=data['city'],
        user_id=user_id
    )
    db.session.add(profile)
    db.session.commit()
    return jsonify({"msg": "Profile Created"}), 201

@app.route('/users', methods=['GET'])
def get_all_user():
    users = User.query.all()
    if not users:
        return jsonify({"error": "User not found"}), 404
    return jsonify([
        {
            "id":u.id,
            "username":u.username
        } for u in users
    ])

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "profile": {
            "age": user.profile.age,
            "city": user.profile.city
        } if user.profile else None
    })


if __name__ == '__main__':
    app.run(debug=True)