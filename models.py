"""
Models Module: This module contain every relation include SqlAlchemy Models and Marsmallow Relations,
this model can be imported to call model for every table(object) needed for return structure object model
"""
from config import db, ma
from marshmallow import fields

#Sql Alchemy Models
#https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
class Directors(db.Model):
    __tablename__ = 'directors'
    name = db.Column(db.String(60), index = True)
    id = db.Column(db.Integer, primary_key = True)
    gender = db.Column(db.Integer, nullable = False)
    uid = db.Column(db.Integer, nullable = False)
    department = db.Column(db.String(60), default = 'Directing')
    movies = db.relationship(
        'Movies',
        backref='director',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Movies.id)'
    )

class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key = True)
    original_title = db.Column(db.String, nullable = False)
    budget = db.Column(db.Integer, default = 0)
    popularity = db.Column(db.Integer, default = 0)
    release_date = db.Column(db.String(60), nullable = False)
    revenue = db.Column(db.Integer, default = 0)
    title = db.Column(db.String(60), nullable = False)
    vote_average = db.Column(db.Float, default = 0)
    vote_count = db.Column(db.Integer, default = 0)
    overview = db.Column(db.String(60), nullable = False)
    tagline = db.Column(db.String(60), nullable = False)
    uid = db.Column(db.Integer, nullable = False)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))

#https://flask-marshmallow.readthedocs.io/en/latest/
# Marsmallow relationship
class DirectorsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Directors
        sqla_session = db.session
        load_instance = True

    movies = fields.Nested('TMoviesSchema', dump_default=[], many=True)

class MoviesSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Movies
        sqla_session = db.session
        load_instance = True

    director = fields.Nested("TDirectorsSchema", dump_default=None)

class TMoviesSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    original_title = fields.Str()
    budget = fields.Int()
    popularity = fields.Int()
    release_date = fields.Str()
    revenue = fields.Int()
    title = fields.Str()
    vote_average = fields.Float()
    vote_count = fields.Int()
    overview = fields.Str()
    tagline = fields.Str()
    uid = fields.Int()
    director_id = fields.Int()

class TDirectorsSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    name = fields.Str()
    id = fields.Int()
    gender = fields.Int()
    uid = fields.Int()
    department = fields.Str()