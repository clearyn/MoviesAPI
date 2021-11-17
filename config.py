import os
import connexion

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#Base directory project
basedir = os.path.abspath(os.path.dirname(__file__))

# Create the Connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance & Configure SQLAlchemy
app = connex_app.app
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nkyiumlhkukrjg:98422bf9d123a9160d85c595e2f4d9d10799b51468ec066512d6a9ec1488b070@ec2-52-204-72-14.compute-1.amazonaws.com:5432/d259va9fbi5tjv'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)