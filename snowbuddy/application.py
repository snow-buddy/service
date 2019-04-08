import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import enum
from sqlalchemy import Integer, Enum
from flask import request, json
from passlib.apps import custom_app_context as pwd_context


app = Flask(__name__, instance_relative_config=True)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "snowbuddy.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass


class ExperienceLevel(enum.Enum):
    beginner = 1
    intermediate = 2
    expert = 3

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    ski_level = db.Column(db.Enum(ExperienceLevel))
    snowboard_level = db.Column(db.Enum(ExperienceLevel))
    num_children = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        return '<User {0} {1} {2} {3} {4} {5}>'.format(self.id, self.first_name,
            self.last_name, self.email, self.ski_level, self.snowboard_level)

@app.route('/register', methods=['POST'])
def register():
    user = User(email=request.json['email'],
        first_name = request.json['first_name'],
        last_name = request.json['last_name'],
        ski_level = request.json['ski_level'],
        snowboard_level = request.json['snowboard_level'],
        num_children = request.json['num_children'])
    password = request.json['password']
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    response = app.response_class(
            response=json.dumps({'user_id': user.id}),
            status=200,
            mimetype='application/json'
            )
    return response
