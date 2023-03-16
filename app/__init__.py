from dotenv import dotenv_values
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


app = Flask(__name__)
config = dotenv_values(".env")
app.config.from_mapping(config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
cors = CORS(app)

from app import models, users

app.register_blueprint(users.blueprint)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
