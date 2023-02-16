from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime

db = SQLAlchemy()


def init_app(app):
    db.app = app
    db.init_app(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    api_key = db.Column(db.String(255), unique=True, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    authenticated = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f'<user {self.id}, {self.email}>'

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'api_key': self.api_key,
            'is_active': self.is_active,
        }

    def update_api_key(self):
        self.api_key = generate_password_hash(self.email + str(datetime.utcnow()))