from flask import Flask, g
import models
from routes import user_blueprint
from flask_migrate import Migrate
from flask_login import LoginManager
from flask.sessions import SecureCookieSessionInterface
import os

app = Flask(__name__)

file_path = os.path.abspath(os.getcwd()) + "./database/user.db"
app.config['SECRET_KEY'] = 'J3QUtmmQtXHL5P52Llf12w'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
models.init_app(app)

app.register_blueprint(user_blueprint)
migrate = Migrate(app, models.db)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.filter_by(id=user_id).first()


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        user = models.User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    return None


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""

    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args,
                                                                **kwargs)


# app.session_interface = CustomSessionInterface()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
