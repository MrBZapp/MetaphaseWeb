from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, types
import hashlib
from datetime import datetime as dt

db = SQLAlchemy()


class entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(Integer, primary_key=True)
    datetime = db.Column(types.DATETIME)
    author = db.Column(String)
    title = db.Column(String)
    headIMG = db.Column(String, nullable=True)
    content = db.Column(types.Text(), nullable=True)
    comment_count = db.Column(Integer)

    def __init__(self, author, title, content):
        self.datetime = dt.now()
        self.author = author
        self.title = title
        self.content = content

    def __repr__(self):
        return "<entry(date='%s', author='%s', title='%s')>" % (self.datetime, self.author, self.title)


class User(db.Model):
    __tablename__ = 'user'
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
    __tablename__ = 'comments'

    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer)
    datetime = db.Column(types.DATETIME)
    content = db.Column(types.TEXT)
    rank = db.Column(Integer)
    post_id = db.Column(Integer)
    comment_count = db.Column(Integer, default=0)

    def __init__(self, user_id, content, post_id):
        self.user_id = user_id
        self.content = content
        self.post_id = post_id
        self.datetime = dt.now()
        self.comment_count = 0

    def __repr__(self):
        return '<Comment by %r for post_id %r' % (self.user_id, self.post_id)