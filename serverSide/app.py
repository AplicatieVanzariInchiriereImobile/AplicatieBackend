from flask import Flask
from serverSide.models import db, User

app = Flask(__name__)
db.init_app(app)
db.create_all()