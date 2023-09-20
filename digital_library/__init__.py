
from flask import Flask
from .site.routes import site
from .authentication.routes import auth
from .api.routes import api
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .models import db as root_db,login_manager, ma

from flask_marshmallow import Marshmallow

from flask_cors import CORS
from digital_library.helpers import JSONEncoder

# Load env variables
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

app.config.from_object(Config)

# Initialize db
root_db.init_app(app)

with app.app_context():
    root_db.create_all()

# Migrate 
migrate = Migrate(app, root_db)

login_manager.init_app(app)
login_manager.login_view = 'auth.signin'

ma.init_app(app)
app.json_encoder = JSONEncoder
CORS(app)