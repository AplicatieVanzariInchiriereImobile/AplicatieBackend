from flask import Flask, request, abort, jsonify, session
from models import db, User
from config import ApplicationConfig
from flask_bcrypt import Bcrypt
from flask_session import Session

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

#sesiune
server_session = Session(app)

bcrypt = Bcrypt(app)
db.init_app(app)

with app.app_context():
    db.create_all()

#get data de la user
@app.route("/loggedUserData", methods=["GET"])
def get_logged_user():
    #daca e sesiune invalida returneaza None
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"Error": "User_id not found"}), 404
    
    user = User.query.filter_by(id = user_id).first()

    return jsonify({
        "id": user.id,
        "email": user.email
    })


@app.route("/register", methods=["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]

    #daca userul cu credentialele astea exista
    user_exists = User.query.filter_by(email = email).first() is not None

    #daca exista deja un user cu credentiale, trimitem status de conflict
    if user_exists:
        #abort(409)
        return jsonify({"Error": "User already exists"}), 409

    #cream user nou
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email = email, password = hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    })

@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user_exists = User.query.filter_by(email = email).first()
    if user_exists is None:
        return jsonify({"Error": "User not found"}), 404
    
    #print(user_exists.email + " " + user_exists.password)
  
    if not bcrypt.check_password_hash(user_exists.password, password):
        return jsonify({"Error": "Incorrect password"}), 401

    #stocare de date despre user in sesiune, dupa ce se logheaza
    session["user_id"] = user_exists.id

    return jsonify({
        "id": user_exists.id,
        "email": user_exists.email
    })

if __name__ == "__main__":
    app.run(debug = True)