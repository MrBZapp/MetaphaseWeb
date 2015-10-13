__author__ = 'Matt Zapp'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from migrate import *
from util import DictDiff

# Global definitions
GLOBAL_ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# Static Subfolder names
POST_IMG_FOLDER = '/static/posts/img/'
POST_TMP_FOLDER = '/static/posts/tmp'
PROJECT_TMP_FOLDER = 'static/projects/tmp'
PROJECT_IMG_FOLDER = 'static/projects/img'

# Config dependent paths
DATABASE_URI = 'sqlite:///database/metaphase.db'

# Create the app and blank database
app = Flask(__name__)
db = SQLAlchemy(app)

# Assign the configuration parameters
app.config['POST_TMP_FOLDER'] = POST_TMP_FOLDER
app.config['POST_IMG_FOLDER'] = POST_IMG_FOLDER

app.config['PROJECT_TMP_FOLDER'] = PROJECT_TMP_FOLDER
app.config['PROJECT_IMG_FOLDER'] = PROJECT_IMG_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
# set the secret key.  keep this really secret:
app.secret_key = '512cgv&P<T$$(){KMhb637rf6tn{_ube532v55@15-sdfgnhyr76'

# create the database tables if they're not already created
import blogDB
db.create_all()

# make sure the tables are up to date with the current models
"""
models = db.get_binds()
for model in models:
    meta = MetaData()
    table = Table(model, meta, autoload=True, autoload_with=db.engine)
    diff = DictDiff(model.columns, table.columns)

    for new_column in diff.added():
        new_column = model.columns[new_column]
        new_column.create(db.engine)

    for removed_column in diff.removed():
        removed_column = table.columns[removed_column]
        table.c.removed_column.drop()
"""

# import the views
import metaphase.post_management
import metaphase.tagbrowse
import metaphase.user_management
import metaphase.comment_management
import metaphase.project_management
import metaphase.about
import metaphase.home
