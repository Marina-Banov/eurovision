from flask import Blueprint, request
from sqlalchemy.exc import StatementError

from app import db, models

blueprint = Blueprint('users', __name__)


@blueprint.route('/users', methods=['POST'])
def add():
    data = request.get_json()
    u = models.User(username=data['username'])
    try:
        db.session.add(u)
        db.session.commit()
        return {}, 200
    except StatementError as e:
        return {"message": str(e.orig)}, 400
