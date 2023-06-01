from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from os import environ
from secret.secret import SECRET_KEY, OPENAI_API_KEY
import openai
import logging
from werkzeug.security import generate_password_hash

if (environ.get("TESTING")):
    # use memory
    DB_NAME = ":memory:"
    log = logging.getLogger('werkzeug')
    log.disabled = True
else:
    DB_NAME = "database.db"
    

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

openai.api_key = OPENAI_API_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

app.app_context().push()


# Database
# Required for SQLite
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)

# Websockets
socket_io = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User  # noqa


@login_manager.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))

@login_manager.unauthorized_handler
# route on not logged in
def unauthorized():
    return redirect("/login", code=302)

from app import views  # noqa

with app.app_context():
    if not path.exists(f"instance/{DB_NAME}"):
        db.create_all()
        print("Created database")


# Create GPT userprofile if not already made
gpt_user = User.query.filter_by(username='ChatGPT').first()  # check if ChatGPT user exists
begin_prompt = "You are a helpful AI assistant, named ChatGPT, in a multi user chat channel made for an agile web dev project."
end_prompt = "users invoke you with '/gpt {your name}'"
# if ChatGPT user doesn't exist, create one
if gpt_user is None:
    gpt_user = User(username='ChatGPT', is_GPT=True)
    gpt_user.begin_prompt = begin_prompt
    gpt_user.end_prompt = ""
    db.session.add(gpt_user)
    db.session.commit()
