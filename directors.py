"""
This is the directors module and supports all the REST actions for the
director data
"""

from flask import make_response, abort
from config import db
from models import Directors, DirectorsSchema, Movies


def read_all(limit = None):
    """
    This function responds to a request for /api/directors
    with the complete lists of directors
    :param limit:   limit of data to show
    :return:        json string of list of directors
    """

    # Serialize the data for the response
    def call_data(directors):
        directors_schema = DirectorsSchema(many=True)
        data = directors_schema.dump(directors)
        return data

    # Check if parameter is true
    if isinstance(limit, int) == True:

        # Create the list of people from our data
        directors = Directors.query.order_by(Directors.id).limit(limit).all()
        data = call_data(directors)
        
        return data
    elif limit == None:
        # Create the list of people from our data
        directors = Directors.query.order_by(Directors.id).all()
        data = call_data(directors)

        return data
    # Otherwise, return type inserted
    else:
        abort(404, f"Required parameter id as integer: Found{type(limit)}")


def read_one(id):
    """
    This function responds to a request for /api/directors/{id}
    with one matching id from directors
    :param id: Id of director to find
    :return: director matching id
    """
    # Build the initial query
    director = (
        Directors.query.filter(Directors.id == id)
        .outerjoin(Movies)
        .one_or_none()
    )

    # Did we find a director?
    if director is not None:

        # Serialize the data for the response
        director_schema = DirectorsSchema()
        data = director_schema.dump(director)
        return data

    # Otherwise, nope, didn't find that director
    else:
        abort(404, f"Director not found for Id: {id}")


def create(director):
    """
    This function creates a new director in the directors structure
    based on the passed in director data
    :param director:  director to create in directors structure
    :return:        201 on success, 406 on director exists
    """
    name = director.get("name")
    gender = director.get("gender")
    uid = director.get("uid")
    department = director.get("department")

    existing_director = (
        Directors.query.filter(Directors.name == name)
        .filter(Directors.gender == gender)
        .filter(Directors.uid == uid)
        .filter(Directors.department == department)
        .one_or_none()
    )

    # Can we insert this director?
    if existing_director is None:

        # Create a director instance using the schema and the passed in director
        schema = DirectorsSchema()
        new_director = schema.load(director, session=db.session)

        # Add the directordirector to the database
        db.session.add(new_director)
        db.session.commit()

        # Serialize and return the newly created director in the response
        data = schema.dump(new_director)

        return data, 201

    # Otherwise, nope, director exists already
    else:
        abort(409, f"Director with name: {name},gender: {gender}, uid:{uid}, department: {department} already exists")


def update(id, director):
    """
    This function updates an existing director in the directors structure
    :param id: Id of the director to update in the directors structure
    :param director: director to update
    :return: updated directors structure
    """
    # Get the director requested from the db into session
    update_director = Directors.query.filter(
        Directors.id == id
    ).one_or_none()

    # Did we find an existing director?
    if update_director is not None:

        # turn the passed in director into a db object
        schema = DirectorsSchema()
        update = schema.load(director, session=db.session)

        # Set the id to the director we want to update
        update.id = update_director.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated director in the response
        data = schema.dump(update_director)

        return data, 200

    # Otherwise, nope, didn't find that director
    else:
        abort(404, f"Director not found for Id: {id}")


def delete(id):
    """
    This function deletes a persdirectoron from the people structure
    :param id: Id of the director to delete
    :return: 200 on successful delete, 404 if not found
    """
    # Get the director requested
    director = Directors.query.filter(Directors.id == id).one_or_none()

    # Did we find a director?
    if director is not None:
        db.session.delete(director)
        db.session.commit()
        return make_response(f"Director {id} deleted", 200)

    # Otherwise, nope, didn't find that director
    else:
        abort(404, f"Director not found for Id: {id}")