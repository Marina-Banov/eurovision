from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(2))
    name = db.Column(db.String(128))
    artist = db.Column(db.Unicode(128))
    song = db.Column(db.Unicode(128))
    songUrl = db.Column(db.String(256))
    inFinal = db.Column(db.Boolean)
    order = db.Column(db.Integer)

    def __repr__(self):
        return '<Country {}>'.format(self.name)

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
