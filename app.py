from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "sqlite_connection"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    muname = db.Column(db.String(200), nullable=False)
    memail = db.Column(db.String(200), nullable=True)  # <--- FIXED

    def to_dict(self):
        return {
            "id": self.id,
            "muname": self.muname,
            "memail": self.memail
        }
@app.route('/todo', methods=['POST'])
def create_todo():
    data = request.get_json()

    uname = data.get('username')
    uemail = data.get('email')

    if not uname:
        return jsonify({"error": "username is required"}), 400

    todo = Todo(muname=uname, memail=uemail)
    db.session.add(todo)
    db.session.commit()

    return jsonify({
        "message": "Todo created successfully",
        "todo": todo.to_dict()
    }), 201

@app.route('/get_todo', methods=['GET'])
def get_todo():
    todos = Todo.query.all()
    return jsonify([t.to_dict() for t in todos]), 200
# -----------------------for update-----------------
@app.route('/todo/<int:u_id>', methods=['PUT'])
def update_todo(u_id):
    todo = Todo.query.get(u_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    data = request.get_json() 
    new_uname = data.get('new_username')  
    new_uemail = data.get('new_uemail')  
    if not new_uname or not new_uemail:
        return jsonify({"error": "username and uemail are required"}), 400    
    todo.muname = new_uname
    todo.memail = new_uemail
    db.session.commit()
    return jsonify({
        "message": "Todo updated successfully",
        "todo": todo.to_dict()
    }), 200
@app.route('/delete_todo/<int:u_id>',methods=['DELETE'])
def delete_user(u_id):
    todo = Todo.query.get(u_id)
    if not todo:
        return jsonify({
            "error":"todo not found to delete"
        }),404
    db.session.delete(todo)
    db.session.commit()    
    return jsonify({
        "message":"user deleted sucessfully",
        "todo":todo.to_dict()
    }),200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
