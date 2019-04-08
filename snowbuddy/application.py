import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import enum
from sqlalchemy import Integer, Enum
from flask import request, json

app = Flask(__name__, instance_relative_config=True)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "snowbuddy.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

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
    db.session.add(user)
    db.session.commit()
    response = app.response_class(
            response=json.dumps({'user_id': user.id}),
            status=200,
            mimetype='application/json'
            )
    return response
