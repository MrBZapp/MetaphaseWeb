__author__ = 'Matt Zapp'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Global definitions
GLOBAL_ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# Static Subfolder names
POST_IMG_FOLDER = '/static/posts/img/'
POST_TMP_FOLDER = '/static/posts/tmp'
PROJECT_TMP_FOLDER = 'static/projects/tmp'
PROJECT_IMG_FOLDER = 'static/projects/IMG'

# Config dependent paths
#DATABASE_URI = 'mysql+pymysql://web-server:m3tadmin@localhost/blogdata' #Production
DATABASE_URI = 'mysql+pymysql://admin:admin@127.0.0.1:63306/blogdata' #Dev

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

# create the database tables
import blogDB
db.create_all()

# import the views
import metaphase.post_management
import metaphase.user_management
import metaphase.comment_management
import metaphase.projects
import metaphase.home

