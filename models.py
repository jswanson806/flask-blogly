"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

# connect our app with SQLAlchemy instance
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""

    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User id ={u.id} first_name={u.first_name} last_name={u.last_name} profile_img = {u.profile_img}>"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String,
                            nullable=False)
    last_name = db.Column(db.String,
                            nullable=False)
    profile_img = db.Column(db.String,
                            nullable=True)
