from metaphase import db
from sqlalchemy import Integer, String, types
import hashlib
from datetime import datetime as dt

# helper table for storing tags
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), nullable=False),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # Tag ID
    value = db.Column(db.String(144), unique=True, nullable=False)   # Tag name

    def __init__(self, value):
        self.value = value


class User(db.Model):
    """Database Model of a Blog User."""
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(144), nullable=False)
    real_name = db.Column(String(144), nullable=False)
    email = db.Column(String(144), nullable=False)
    _hash = db.Column(String(144), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    _admin = db.Column(Integer)

    def __init__(self, username, real_name, email, password):
        self.username = username
        self.real_name = real_name
        self.email = email
        self._hash = hashlib.sha224(username + password).hexdigest()
        self._admin = False

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    """Database Model of a blog post or comment"""
    id = db.Column(Integer, primary_key=True)
    project_id = db.Column('Project', db.ForeignKey('project.id'))
    parent_id = db.Column(Integer, db.ForeignKey('post.id'))
    author_id = db.Column(Integer, db.ForeignKey('user.id'))
    author_str = db.Column(String(144))
    title = db.Column(String(144), nullable=True)
    content = db.Column(types.Text(), nullable=False)
    datetime = db.Column(types.DATETIME)
    comment_count = db.Column(Integer)
    rank = db.Column(Integer)
    parent = db.relationship('Post', remote_side=[id])
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, user, content, title=None, parent=None):
        """
        :param user: the User class object of the author of the post or comment
        :param content: the body of the post or comment
        :param parent: the parent of the comment
        ONLY USED IN POSTINGS, NOT COMMENTS:
        :param title: the tile of the post
        :return: <Post>
        """
        self.author_id = user.id
        self.author_str = user.username
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

    def __repr__(self):
        return "<Post(date='%s', author='%s', title='%s')>" % (self.datetime, self.author_id, self.title)


class Project(db.Model):
    """Database Model of a full project"""
    id = db.Column(Integer, primary_key=True)   # ID of the project
    title = db.Column(String(144), nullable=False)  # Title of the project
    pict = db.Column(String(144), nullable=False)   # Tile picture of the project
    abstract = db.Column(types.Text(), nullable=False)  # Tile Abstract of the project
    rel_files = db.Column(types.Text())  # CSV of related file paths
    rel_posts = db.relationship('Post', remote_side=[id])  # Posts related to the project
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('projects', lazy='dynamic'))

    def __init__(self, title, pict, abstract):
        """
        :param title: the name of the project, or one-liner.
        :param pict: a headline picture for the jorb.
        :param abstract: a quick abstract about the project
        """
        self.title = title
        self.pict = pict
        self.abstract = abstract

    def __repr__(self):
        return "<Project(title='%s')>" % self.title