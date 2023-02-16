from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.app = app
    db.init_app(app)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    contact_name = db.Column(db.String(128))
    contact_email = db.Column(db.String(128))
    contact_number = db.Column(db.String(16))

    def serialize(self):
        return {
            "user_id": self.user_id,
            "contact_name": self.contact_name,
            "contact_number": self.contact_number,
            "contact_email": self.contact_email
        }


class ClientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Client
