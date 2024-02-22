from flask_login import LoginManager

from configuration.core.config import base_config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db_user = base_config.DB_USER
db_pass = base_config.DB_PASS
db_name = base_config.DB_NAME
db_port = base_config.DB_PORT
db_host = base_config.DB_HOST


flask_app = Flask(__name__)
flask_app.config["SECRET_KEY"] = base_config.SECRET
flask_app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

flask_db = SQLAlchemy()
flask_db.init_app(flask_app)

login_manager = LoginManager()
login_manager.init_app(flask_app)
