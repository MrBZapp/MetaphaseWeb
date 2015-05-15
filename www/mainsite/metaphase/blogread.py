from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, types
import hashlib
from datetime import datetime as dt

from metaphase import app

db = SQLAlchemy(app)

class Entry(db.Model):

    id = db.Column(Integer, primary_key=True)
    datetime = db.Column(types.DATETIME)
    author = db.Column(String(45))
    title = db.Column(String(144))
    headIMG = db.Column(String(144), nullable=True)
    content = db.Column(types.Text(), nullable=True)
    comment_count = db.Column(Integer)

    def __init__(self, author, title, content, imgpath):
        self.datetime = dt.now()
        self.author = author
        self.title = title
        self.content = content
        self.headIMG = imgpath

    def __repr__(self):
        return "<entry(date='%s', author='%s', title='%s')>" % (self.datetime, self.author, self.title)


class User(db.Model):
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(144), nullable=False)
    realname = db.Column(String(45))
    email = db.Column(String(144), nullable=False)
    _hash = db.Column(String(144), nullable=False)
    _admin = db.Column(Integer)

    def __init__(self, username, name, email, password):
        self.username = username
        self.realname = name
        self.email = email
        self._hash = hashlib.sha224(username + password).hexdigest()
        self._admin = False

    def __repr__(self):
        return '<User %r>' % self.username

class Comment(db.Model):

    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer)
    datetime = db.Column(types.DATETIME)
    content = db.Column(types.TEXT)
    rank = db.Column(Integer)
    post_id = db.Column(Integer)

    def __init__(self, post_id, content, user_id):
        self.post_id = post_id
        self.content = content
        self.user_id = user_id
        self.datetime = dt.now()
        self.rank = 1

    def __repr__(self):
        return '<Comment by %r for post_id %r' % (self.user_id, self.post_id)
