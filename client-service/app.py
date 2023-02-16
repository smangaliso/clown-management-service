from flask import Flask
from flask_migrate import Migrate
import models
from routes import client_blueprint
import os

app = Flask(__name__)

file_path = os.path.abspath(os.getcwd()) + "./database/client.db"
app.config['SECRET_KEY'] = 'J3QUtmmQtXHL5P52Llf12w'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
models.init_app(app)

app.register_blueprint(client_blueprint)
migrate = Migrate(app, models.db)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
