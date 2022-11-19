"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime

# connect our app with SQLAlchemy instance
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Table for users.
    
    >>> id = db.Integer, primary_key=True
    >>> first_name = db.String, nullable=False
    >>> last_name = db.String, nullable=False
    >>> profile_img = db.String, nullable=True
    >>> posts = db.relationship('Post', backref='users', cascade='all, delete-orphan')
    
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                    primary_key=True)
    first_name = db.Column(db.String,
                            nullable=False)
    last_name = db.Column(db.String,
                            nullable=False)
    profile_img = db.Column(db.String,
                            nullable=True)
    posts = db.relationship('Post', backref='users', cascade='all, delete-orphan')

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} profile_img = {u.profile_img}>"
    
    
class Post(db.Model):
    """Table for posts.

    >>> id = db.Integer, primary_key=True, autoincrement=True
    >>> title = db.Text, nullable=False
    >>> content = db.Text, nullable=False
    >>> created_at = db.DateTime, nullable=False, default=datetime.now()
    >>> user_id = db.Integer, db.ForeignKey('users.id'), nullable=False
    >>> tags = db.relationship('Tag', secondary='post_tags', backref='posts')

    """

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.Text,
                        nullable=False)
    content = db.Column(db.Text,
                            nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user_id = db.Column(db.Integer,
                            db.ForeignKey('users.id'), nullable=False)

    assignments = db.relationship('PostTag', backref='posts')
    
    tags = db.relationship('Tag', secondary='post_tags', backref='posts')

    def __repr__(self):
        return f"< Post id= {self.id} title= {self.title} created_at= {self.created_at} >"


class PostTag(db.Model):
    """Through relationship table for Post and Tag.
    
    >>> post_id = db.Integer, db.ForeignKey('posts.id'), primary_key=True
    >>> tag_id = db.Integer, db.ForeignKey('tags.id'), primary_key=True


    """

    __tablename__ = "post_tags"

    # PK, foreign key to posts.id
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    # PK, foreign key to tags.id
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    


class Tag(db.Model):
    """Table for tags.
    
    >>> id = db.Integer, primary_key=True,  autoincrement=True
    >>> name = db.Text, unique=True, nullable=False
    >>> assignments = db.relationship('PostTag', backref='tags')
    
    """

    __tablename__ = "tags"

    id = db.Column(db.Integer, 
                    primary_key=True, 
                    autoincrement=True)
    name = db.Column(db.Text,
                        unique=True,
                        nullable=False)

    assignments = db.relationship('PostTag', backref='tags', cascade='all, delete-orphan')


    def __repr__(self):
        return f"< Tag id= {self.id} name= {self.name}>"