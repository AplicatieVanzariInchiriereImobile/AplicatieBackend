from flask import Flask, request, abort, jsonify, session
from models import db, User, Vanzari
from config import ApplicationConfig
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

cors = CORS(app, supports_credentials=True)

#sesiune
server_session = Session(app)

bcrypt = Bcrypt(app)
db.init_app(app)

with app.app_context():
    db.create_all()
    #Vanzari.__table__.drop(db.engine)

#get data de la user
@cross_origin
@app.route("/loggedUserData", methods=["GET"])
def get_logged_user():
    #daca e sesiune invalida returneaza None
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"Error": "User_id not found"}), 404
    
    user = User.query.filter_by(id = user_id).first()

    return jsonify({
        "id": user.id,
        "email": user.email,
        "name" : user.name,
        "role": user.role
    })

@cross_origin
@app.route("/register", methods=["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]
    name = request.json["name"]

    #daca userul cu credentialele astea exista
    user_exists = User.query.filter_by(email = email).first() is not None

    #daca exista deja un user cu credentiale, trimitem status de conflict
    if user_exists:
        #abort(409)
        return jsonify({"Error": "User already exists"}), 409

    #cream user nou
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email = email, password = hashed_password, name = name, role = "client")
    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.id

    return jsonify({
        "id": new_user.id,
        "email": new_user.email,
        "name" : new_user.name,
        "role" : new_user.role
    })

@cross_origin
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
        "email": user_exists.email,
        "name": user_exists.name,
        "role": user_exists.role
    })

@cross_origin
@app.route("/logout", methods=["POST"])
def logout():

    #session.pop("user_id")
    return "200"



@cross_origin
@app.route("/getVanzari", methods=["GET"])
def get_Vanzari():
    
    vanzari = Vanzari.query.filter_by().all()
    #print(vanzari[0].descriere)

    return jsonify(lista_vanzari = [Vanzari.serialize(vanzare) for vanzare in vanzari])

    #return jsonify(vanzari, status=200, mimetype='application/json')


@cross_origin
@app.route("/insertVanzari", methods=["POST"])
def insert_vanzari():
    descriere = request.json["descriere"]
    adresa = request.json["adresa"]
    pret = request.json["pret"]
    tip = request.json["tip"]

    print(descriere)
    print(adresa)
    print(pret)

    vanzari_exists = Vanzari.query.filter_by(adresa = adresa).first() is not None

    #daca exista deja un user cu credentiale, trimitem status de conflict
    if vanzari_exists:
        #abort(409)
        return jsonify({"Error": "Vanzari already exists"}), 409

    new_vanzari = Vanzari(descriere = descriere, adresa = adresa, pret = pret, tip=tip)
    db.session.add(new_vanzari)
    db.session.commit()

    return jsonify({
        "id": new_vanzari.id,
        "descriere": new_vanzari.descriere,
        "adresa": new_vanzari.adresa,
        "pret": new_vanzari.pret,
        "tip": new_vanzari.tip
    })



@cross_origin
@app.route("/updateVanzari", methods=["POST"])
def update_vanzari():
    descriere = request.json["descriere"]
    adresa = request.json["adresa"]
    pret = request.json["pret"]
    tip = request.json["tip"]

    vanzari_exists = Vanzari.query.filter_by(adresa = adresa).first()
    if vanzari_exists is None:
        return jsonify({"Error": "Vanzari not found"}), 404
    
    vanzari_exists.descriere = descriere
    vanzari_exists.pret = pret
    vanzari_exists.tip = tip
    db.session.commit()

    return jsonify({
        "id": vanzari_exists.id,
        "descriere": vanzari_exists.descriere,
        "adresa": vanzari_exists.adresa,
        "pret": vanzari_exists.pret,
        "tip": vanzari_exists.tip
    })


@cross_origin
@app.route("/deleteVanzari", methods=["POST"])
def delete_vanzari():
    adresa = request.json["adresa"]

    vanzari_exists = Vanzari.query.filter_by(adresa = adresa).first()
    if vanzari_exists is None:
        return jsonify({"Error": "Vanzari not found"}), 404
    
    db.session.delete(vanzari_exists)
    db.session.commit()

    return jsonify({
        "id": vanzari_exists.id,
        "adresa": vanzari_exists.adresa,
    })

if __name__ == "__main__":
    app.run(debug = True)