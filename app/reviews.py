from flask import Blueprint, request
from flask_cors import cross_origin
from operator import itemgetter
from sqlalchemy import func
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.exc import StatementError, NoResultFound

from app import db, models, config
from app.utils import borda_count, get_reviews_chart

blueprint = Blueprint("reviews", __name__)


@blueprint.route("/reviews/points", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def add_or_update():
    data = request.get_json()
    try:
        sql = insert(models.Review).values(
            userId=data["id"],
            countryId=data["countryId"],
            points=data["points"],
        ).on_conflict_do_update(
            index_elements=["userId", "countryId"],
            set_=dict(points=data["points"])
        )
        db.session.execute(sql)
        db.session.commit()
        return get_reviews_chart(data["countryId"]), 200
    except NoResultFound as e:
        return {"message": str(e)}, 404
    except StatementError as e:
        return {"message": str(e.orig)}, 400


@blueprint.route("/reviews/order", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def new_order():
    data = request.get_json()
    try:
        for i in data["orderlist"]:
            sql = insert(models.Review).values(
                userId=data["id"],
                countryId=i["countryId"],
                order=i["order"],
            ).on_conflict_do_update(
                index_elements=["userId", "countryId"],
                set_=dict(order=i["order"])
            )
            db.session.execute(sql)
        db.session.commit()
        return {}, 200
    except NoResultFound as e:
        return {"message": str(e)}, 404
    except StatementError as e:
        return {"message": str(e.orig)}, 400


@blueprint.route("/reviews", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def get():
    try:
        reviews = db.session.query(
            models.Review.countryId,
            func.sum(models.Review.points).label("points"),
            func.group_concat(models.Review.order).label("order")) \
            .join(models.Country) \
            .filter(models.Country.inFinal) \
            .filter(models.Country.year == int(config["EUROVISION_YEAR"])) \
            .group_by(models.Review.countryId).all()
        return {
            "pointlist": sorted(
                [{"countryId": i[0], "points": i[1] or 0} for i in reviews],
                key=itemgetter("points"),
                reverse=True,
            ),
            "orderlist": borda_count(
                [{"countryId": i[0], "order": i[2]} for i in reviews],
            ),
        }, 200
    except NoResultFound as e:
        return {"message": str(e)}, 404
    except StatementError as e:
        return {"message": str(e.orig)}, 400
