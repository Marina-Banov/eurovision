from operator import itemgetter
from flask import Blueprint, request
from sqlalchemy.exc import StatementError, NoResultFound
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import func
from flask_cors import cross_origin

from app import db, models, config

blueprint = Blueprint("reviews", __name__)


@blueprint.route("/reviews/points", methods=["POST"])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
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
        chart = db.session.query(
            models.Review.points,
            func.count(models.Review.id)) \
            .group_by(models.Review.points) \
            .filter(models.Review.countryId == data["countryId"]).all()
        return {i[0]: i[1] for i in chart}, 200
    except NoResultFound as e:
        return {"message": str(e)}, 404
    except StatementError as e:
        return {"message": str(e.orig)}, 400


@blueprint.route("/reviews/order", methods=["POST"])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
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
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def get():
    try:
        reviews = db.session.query(
            models.Review.countryId,
            func.sum(models.Review.points).label("points"),
            func.group_concat(models.Review.order).label("order")) \
            .join(models.Country) \
            .filter(models.Country.inFinal)\
            .filter(models.Country.year == int(config["EUROVISION_YEAR"]))\
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


def borda_count(ranked_items):
    n = len(ranked_items)
    for i, item in enumerate(ranked_items):
        ranked_items[i]["order"] = sum([
            n - int(op) for op in item["order"].split(",")
        ])
    ranked_items.sort(key=itemgetter("order"), reverse=True)
    for i, item in enumerate(ranked_items):
        ranked_items[i]["order"] = i + 1
    return ranked_items
