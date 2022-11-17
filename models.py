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
    """User."""

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
    """Post."""

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

    

    def __repr__(self):
        return f"< Post id= {self.id} title= {self.title} created_at= {self.created_at} >"
