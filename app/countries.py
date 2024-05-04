from flask import Blueprint, request
from flask_cors import cross_origin
from sqlalchemy.exc import StatementError, NoResultFound

from app import db, models, config
from app.utils import get_reviews_chart

blueprint = Blueprint("countries", __name__)


@blueprint.route("/countries", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def get():
    data = request.args.get("id", None)
    try:
        if data:
            country = db.session.query(models.Country) \
                .filter(models.Country.id == data).one()
            country = country.__dict__
            country.pop("_sa_instance_state")
            country["pointlist"] = get_reviews_chart(data)
            return country, 200
        else:
            countries = db.session.query(models.Country) \
                .filter(models.Country.inFinal) \
                .filter(models.Country.year == int(config["EUROVISION_YEAR"])) \
                .order_by(models.Country.order).all()
            for i in range(len(countries)):
                countries[i] = countries[i].__dict__
                countries[i].pop("_sa_instance_state")
            return {"countries": countries}, 200
    except NoResultFound as e:
        return {"message": str(e)}, 404
    except StatementError as e:
        return {"message": str(e.orig)}, 400
