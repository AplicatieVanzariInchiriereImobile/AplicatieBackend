from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    name = db.Column(db.String(300), unique=False)
    email = db.Column(db.String(300), unique=True)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(300), unique=False)


class Vanzari(db.Model):
    __tablename__ = "Vanzari"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    descriere = db.Column(db.String(300), unique=False)
    adresa = db.Column(db.String(300), unique=False)
    pret = db.Column(db.Integer, unique=False)
    tip = db.db.Column(db.String(300), unique=False)

    def serialize(self):
        return {
            'id': self.id,
            'descriere': self.descriere,
            'adresa': self.adresa,
            'pret': self.pret,
            'tip': self.tip
        }

