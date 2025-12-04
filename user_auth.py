from flask import Flask, request, jsonify ,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
app = Flask(__name__)
app.secret_key = "mysecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///auth.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)



# ----------------- Login Required Decorator -----------------
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return jsonify({"error": "Login required"}), 401

        return f(*args, **kwargs)
    return wrapper

# -----------------user regisration----------------------
@app.route('/register',methods=['POST'])
def user_register():
    data = request.get_json()
    
    uname = data.get('username')
    email = data.get('email')
    password = data.get('password')


    if not uname or not email or not password:
        return jsonify({
            "error":"required all fields"
        }),400
    if User.query.filter_by(email=email).first():
        return jsonify({
            "error":"email already register"
        }),400
    if User.query.filter_by(username=uname).first():
         return jsonify({
            "error":"username already register"
        }),400


    hash_pass = generate_password_hash(password)
    users = User(username=uname,email=email,password=hash_pass)
    db.session.add(users)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# --------------------------for login user---------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Email & password required"}), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Incorrect password"}), 401
    
    session["user_id"] = user.id
    session["username"] = user.username
    return jsonify({"message": "Login successful", "username": user.username}), 200


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    return jsonify({
        "message": "You are logged in!",
        "user_id": session["user_id"],
        "username": session["username"]
    })


# ----------------- Logout Route -----------------
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    return jsonify({"message": "Logout successful"}), 200













with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)