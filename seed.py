"""Seed file to make sample data for users db."""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()


# Add users
darkphoenix = User(first_name='Jean', last_name='Grey', profile_img='https://www.denofgeek.com/wp-content/uploads/2017/09/x-men_jean_grey_dark_phoenix.jpg?resize=768%2C432')
cyclops = User(first_name='Scott', last_name='Summers', profile_img='https://thicc.mywaifulist.moe/waifus/22392/6d9f45b40176c8c62cacde09f863acce45cfb2fa0f44564afa0dbfac4017753e_thumb.jpeg')
professorx = User(first_name='Charles', last_name='Xaviar', profile_img='https://screenrant.com/wp-content/uploads/professor-x.jpg')

# Add posts
p1 = Post(title='First Post', content='First content', user_id=1)
p2 = Post(title='Second Post', content='Second content', user_id=1)
p3 = Post(title='Third Post', content='Third content', user_id=2)

# Add new objects to session, so they'll persist
db.session.add(darkphoenix)
db.session.add(cyclops)
db.session.add(professorx)

# Commit--otherwise, this never gets saved!
db.session.commit()

db.session.add(p1)
db.session.add(p2)
db.session.add(p3)

# Commit--otherwise, this never gets saved!
db.session.commit()