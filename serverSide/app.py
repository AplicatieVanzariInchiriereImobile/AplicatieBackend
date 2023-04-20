from flask import Flask, request, abort, jsonify
from models import db, User
from config import ApplicationConfig
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
db.init_app(app)

with app.app_context():
    db.create_all()


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

    return ""

if __name__ == "__main__":
    app.run(debug = True)