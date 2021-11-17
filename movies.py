"""
This is the movies module and supports all the REST actions for the
movie data
"""

from flask import make_response, abort
from config import db
from models import Movies, MoviesSchema, Directors
from sqlalchemy import desc


def read_all(limit = None):
    """
    This function responds to a request for /api/movies
    with the complete lists of movies
    :param limit: limit of data to show
    :return: json string of list of movies
    """

    # Serialize the data for the response
    def call_data(movies):
        directors_schema = MoviesSchema(many=True)
        data = directors_schema.dump(movies)
        return data

    # Check if parameter is true
    if isinstance(limit, int) == True:

        # Create the list of people from our data
        movies = Movies.query.order_by(Movies.id).limit(limit).all()
        data = call_data(movies)
        
        return data
    elif limit == None:
        # Create the list of people from our data
        movies = Movies.query.order_by(Movies.id).all()
        data = call_data(movies)

        return data
    # Otherwise, return type inserted
    else:
        abort(404, f"Required parameter id as integer: Found{type(limit)}")


def read_one(director_id, movie_id):
    """
    This function responds to a request for
    /api/directors/{director_id}/movies/{movie_id}
    with one matching movie for the associated director
    :param director_id: Id of director the movie is related to
    :param movie_id: Id of the movie
    :return: json string of movie contents
    """
    # Query the database for the movie
    movie = (
        Movies.query.join(Directors, Directors.id == Movies.director_id)
        .filter(Directors.id == director_id)
        .filter(Movies.id == movie_id)
        .one_or_none()
    )

    # Was a movie found?
    if movie is not None:
        movie_schema = MoviesSchema()
        data = movie_schema.dump(movie)
        return data

    # Otherwise, nope, didn't find that movie
    else:
        abort(404, f"Movie not found for director Id: {director_id} with movie Id: {movie_id}")


def create(director_id, movie):
    """
    This function creates a new movie related to the passed in director id.
    :param director_id: Id of the director the movie is related to
    :param movie: The JSON containing the movie data
    :return: 201 on success
    """
    # get the parent director
    director = Directors.query.filter(Directors.id == director_id).one_or_none()

    # Was a director found?
    if director is None:
        abort(404, f"Director not found for Id: {director_id}")

    # Create a movie schema instance
    schema = MoviesSchema()
    new_movie = schema.load(movie, session=db.session)

    # Add the movie to the director and database
    director.movies.append(new_movie)
    db.session.commit()

    # Serialize and return the newly created movie in the response
    data = schema.dump(new_movie)

    return data, 201


def update(director_id, movie_id, movie):
    """
    This function updates an existing movie related to the passed in
    director id.
    :param director_id: Id of the director the movie is related to
    :param movie_id: Id of the movie to update
    :param movie: The JSON containing the movie data
    :return: 200 on success
    """
    update_movie = (
        Movies.query.filter(Directors.id == director_id)
        .filter(Movies.id == movie_id)
        .one_or_none()
    )

    # Did we find an existing movie?
    if update_movie is not None:

        # turn the passed in movie into a db object
        schema = MoviesSchema()
        update = schema.load(movie, session=db.session)

        # Set the id's to the movie we want to update
        update.director_id = update_movie.director_id
        update.id = update_movie.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated movie in the response
        data = schema.dump(update_movie)

        return data, 200

    # Otherwise, nope, didn't find that movie
    else:
        abort(404, f"Movie not found for Id: {director_id}")


def delete(director_id, movie_id):
    """
    This function deletes a movie from the movie structure
    :param director_id: Id of the person the movie is related to
    :param movie_id: Id of the movie to delete
    :return: 200 on successful delete, 404 if not found
    """
    # Get the movie requested
    movie = (
        Movies.query.filter(Directors.id == director_id)
        .filter(Movies.id == movie_id)
        .one_or_none()
    )

    # did we find a movie?
    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return make_response(
            "Movie {movie_id} deleted".format(movie_id=movie_id), 200
        )

    # Otherwise, nope, didn't find that movie
    else:
        abort(404, f"Movie not found for Id: {movie_id}")

def summary(limit, order_by = None):
    """
    This function responds to a request for /api/movies
    with the complete lists of movies
    :param limit: limit of data to show
    :return: json string of list of movies
    """

    # Serialize the data for the response
    def call_data(movies):
        directors_schema = MoviesSchema(many=True)
        data = directors_schema.dump(movies)
        return data

    # Check if parameter is true
    order_by_choices = ['budget', 'revenue', 'popularity']
    if isinstance(limit, int) == True and limit > 0:

        # query by selected order by
        if isinstance(order_by, str) and str(order_by) in order_by_choices:
            movies = Movies.query.order_by(desc(Movies.budget)).limit(limit)
            if order_by == 'revenue':
                movies = Movies.query.order_by(desc(Movies.revenue)).limit(limit)
            elif order_by == 'popularity':
                movies = Movies.query.order_by(desc(Movies.revenue)).limit(limit)
            else:
                movies = Movies.query.order_by(desc(Movies.budget)).limit(limit)
        else:
            abort(404, f"Order by parameter available is ['budget', 'revenue', 'popularity']")
        
        data = call_data(movies)
        return data

    # Otherwise, return error
    else:
        abort(404, f"Required parameter id as integer: Found{type(limit)}")