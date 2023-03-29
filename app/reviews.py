from flask import Blueprint, request
from sqlalchemy.exc import StatementError, NoResultFound
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import func

from app import db, models

blueprint = Blueprint("reviews", __name__)


@blueprint.route("/reviews/points", methods=["POST"])
def add_or_update():
    data = request.get_json()
    try:
        u = db.session.query(models.User) \
            .filter(models.User.username == data["username"]).one()
        sql = insert(models.Review).values(
            userId=u.id,
            countryId=data["countryId"],
            points=data["points"],
        ).on_conflict_do_update(
            index_elements=["userId", "countryId"],
            set_=dict(points=data["points"])
        )
        db.session.execute(sql)
        db.session.commit()
        chart = db.session.query(
            models.Review.points,
            func.count(models.Review.id))\
            .group_by(models.Review.points)\
            .filter(models.Review.countryId == data["countryId"]).all()
        return {i[0]: i[1] for i in chart}, 200
    except NoResultFound as e:
        return {"message": str(e)}, 404
    except StatementError as e:
        return {"message": str(e.orig)}, 400


@blueprint.route("/reviews/order", methods=["POST"])
def new_order():
    data = request.get_json()
    try:
        u = db.session.query(models.User) \
            .filter(models.User.username == data["username"]).one()
        return {}, 200
    except NoResultFound as e:
        return {"message": str(e)}, 404
    except StatementError as e:
        return {"message": str(e.orig)}, 400
