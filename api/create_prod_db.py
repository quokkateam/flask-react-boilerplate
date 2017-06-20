from api import PROD_CONFIG, set_config
from flask import Flask
from models import db

app = Flask(__name__)
set_config(app, PROD_CONFIG)
db.init_app(app)

with app.test_request_context('/'):
    db.create_all()
