from flask import Blueprint, request
from sqlalchemy.exc import StatementError, NoResultFound, IntegrityError
from flask_cors import cross_origin

from app import db, models, config

blueprint = Blueprint("users", __name__)


@blueprint.route("/users", methods=["POST"])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def add():
    data = request.get_json()["username"]
    u = models.User({"username": data})
    try:
        db.session.add(u)
        countries = db.session.query(models.Country) \
            .filter(models.Country.inFinal) \
            .filter(models.Country.year == int(config["EUROVISION_YEAR"])) \
            .order_by(models.Country.order).all()
        for i, c in enumerate(countries):
            r = models.Review({"userId": u.id, "countryId": c.id, "order": i+1})
            db.session.add(r)
        db.session.commit()
        return get(data)
    except IntegrityError:
        db.session.rollback()
        return get(data)[0], 409
    except StatementError as e:
        return {"message": str(e.orig)}, 400


@blueprint.route("/users", methods=["GET"])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def get(username=None):
    data = username or request.args["username"]
    try:
        u = db.session.query(models.User)\
            .filter(models.User.username == data).one()
        reviews = db.session.query(
            models.Review.countryId,
            models.Review.points,
            models.Review.order).filter(models.Review.userId == u.id).all()
        u = u.__dict__
        u.pop("_sa_instance_state")
        u.pop("password_hash")
        u["pointlist"] = [{"countryId": i[0], "points": i[1]} for i in reviews
                          if i[1] is not None]
        u["orderlist"] = [{"countryId": i[0], "order": i[2]} for i in reviews
                          if i[2] is not None]
        return u, 200
    except NoResultFound as e:
        return {"message": str(e)}, 404
    except StatementError as e:
        return {"message": str(e.orig)}, 400
