from operator import itemgetter
from sqlalchemy import func

from app import db, models


def get_reviews_chart(country_id):
    chart = db.session.query(
        models.Review.points,
        func.count(models.Review.id)) \
        .group_by(models.Review.points) \
        .filter(models.Review.points > 0) \
        .filter(models.Review.countryId == country_id).all()
    result = {i[0]: i[1] for i in chart}
    return {i: result.get(i, 0) for i in range(1, 11)}


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
