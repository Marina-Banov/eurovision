from app import db


ignored_keys = ["_sa_instance_state", "year"]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    review = db.relationship("Review", back_populates="user", cascade="all,delete-orphan")

    def __repr__(self):
        return str({
            k: v for k, v in self.__dict__.items() if k not in ignored_keys
        })

    def __init__(self, user):
        self.__dict__.update(user)


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(2))
    name = db.Column(db.String(128))
    artist = db.Column(db.Unicode(128))
    song = db.Column(db.Unicode(128))
    songUrl = db.Column(db.String(256))
    inFinal = db.Column(db.Boolean)
    order = db.Column(db.Integer)
    year = db.Column(db.Integer)
    motherTongue = db.Column(db.Boolean)
    review = db.relationship("Review", back_populates="country", cascade="all,delete-orphan")

    def __repr__(self):
        return str({
            k: v for k, v in self.__dict__.items() if k not in ignored_keys
        })

    def __init__(self, country):
        self.__dict__.update(country)

    @classmethod
    def seed(cls, c):
        country = Country(c)
        db.session.add(country)
        db.session.commit()

    @classmethod
    def clean(cls):
        db.session.query(cls).delete()


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(
        db.ForeignKey("user.id", ondelete="CASCADE", name="userId")
    )
    countryId = db.Column(
        db.ForeignKey("country.id", ondelete="CASCADE", name="countryId")
    )
    points = db.Column(db.Integer)
    order = db.Column(db.Integer)
    user = db.relationship("User", back_populates="review")
    country = db.relationship("Country", back_populates="review")

    __table_args__ = (
        db.UniqueConstraint("userId", "countryId"),
    )

    def __repr__(self):
        return str({
            k: v for k, v in self.__dict__.items() if k not in ignored_keys
        })

    def __init__(self, review):
        self.__dict__.update(review)
