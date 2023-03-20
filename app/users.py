from flask import Blueprint, request
from sqlalchemy.exc import StatementError, NoResultFound, IntegrityError

from app import db, models

blueprint = Blueprint('users', __name__)


@blueprint.route('/users', methods=['POST'])
def add():
    data = request.get_json()['username']
    u = models.User(username=data)
    try:
        db.session.add(u)
        db.session.commit()
        return {}, 200
    except IntegrityError:
        db.session.rollback()
        u = db.session.query(models.User)\
            .filter(models.User.username == data).one()
        return eval(str(u)), 409
    except StatementError as e:
        return {"message": str(e.orig)}, 400


@blueprint.route('/users', methods=['GET'])
def get():
    data = request.args['username']
    try:
        u = db.session.query(models.User)\
            .filter(models.User.username == data).one()
        return eval(str(u)), 200
    except NoResultFound as e:
        return {"message": str(e)}, 404
    except StatementError as e:
        return {"message": str(e.orig)}, 400
