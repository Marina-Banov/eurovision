from flask import Blueprint
from app import db, models

blueprint = Blueprint('users', __name__)


@blueprint.route('/users')
def add():
    u = models.User(username='john2', email='john2@example.com')
    db.session.add(u)
    db.session.commit()
    return 'ok'
