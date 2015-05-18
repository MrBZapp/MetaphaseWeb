from _ast import In
from metaphase import db
from sqlalchemy import Integer, String, types
import hashlib
from datetime import datetime as dt


class User(db.Model):
    """Database Model of a Blog User."""
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


class Post(db.Model):
    """Database Model of a blog post or comment"""
    id = db.Column(Integer, primary_key=True)
    parent_id = db.Column(Integer, db.ForeignKey('post.id'), nullable=True)
    author = db.Column(String(45), db.ForeignKey('user.realname'), nullable=False)
    title = db.Column(String(144), nullable=True)
    headIMG = db.Column(String(144), nullable=True)
    content = db.Column(types.Text(), nullable=False)
    datetime = db.Column(types.DATETIME)
    comment_count = db.Column(Integer)
    rank = db.Column(Integer)
    parent = db.relationship("Post", remote_side=[id])

    def __init__(self, author, content, title=None, img_path=None, parent=None):
        """
        :param author: the author of the post or comment
        :param content: the body of the post or comment
        :param parent: the parent of the comment
        ONLY USED IN POSTINGS, NOT COMMENTS:
        :param title: the tile of the post
        :param img_path: the headline image of the post (DEPRECATED)
        :return: <Post>
        """
        self.author = author
        self.content = content
        self.datetime = dt.now()
        self.comment_count = 0
        self.rank = 1

        if parent is not None:
            self.parent = parent
            self.parent_id = parent.id
            self.parent.comment_count += 1

        if title is not None:
            self.title = title

        if img_path is not None:
            self.headIMG = img_path

    def __repr__(self):
        return "<Post(date='%s', author='%s', title='%s')>" % (self.datetime, self.author, self.title)