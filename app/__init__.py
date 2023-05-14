from dotenv import dotenv_values
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy import create_engine, event


app = Flask(__name__)
config = dotenv_values(".env")
app.config.from_mapping(config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
engine = create_engine("sqlite:///instance/eurovision.db")
event.listen(
    engine,
    'connect',
    lambda dbapi_con, _: dbapi_con.execute('pragma foreign_keys=ON')
)
cors = CORS(app)

from app import users, countries, reviews

app.register_blueprint(users.blueprint)
app.register_blueprint(countries.blueprint)
app.register_blueprint(reviews.blueprint)


@app.after_request
def after_request(response):
    response.access_control_allow_origin = "*"
    return response


if __name__ == "__main__":
    app.run()
