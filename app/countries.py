from flask import Blueprint
from sqlalchemy.exc import StatementError, NoResultFound

from app import db, models, config

blueprint = Blueprint("countries", __name__)


@blueprint.route("/countries", methods=["GET"])
def get():
    try:
        countries = db.session.query(models.Country)\
            .filter(models.Country.inFinal)\
            .filter(models.Country.year == int(config["EUROVISION_YEAR"]))\
            .order_by(models.Country.order).all()
        for i in range(len(countries)):
            countries[i] = countries[i].__dict__
            countries[i].pop("_sa_instance_state")
        return {"countries": countries}, 200
    except NoResultFound as e:
        return {"message": str(e)}, 404
    except StatementError as e:
        return {"message": str(e.orig)}, 400
