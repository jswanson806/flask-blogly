"""Seed file to make sample data for users db."""

from models import User, Post, PostTag, Tag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()
Tag.query.delete()


# Add users
darkphoenix = User(first_name='Jean', last_name='Grey', profile_img='https://www.denofgeek.com/wp-content/uploads/2017/09/x-men_jean_grey_dark_phoenix.jpg?resize=768%2C432')
cyclops = User(first_name='Scott', last_name='Summers', profile_img='https://thicc.mywaifulist.moe/waifus/22392/6d9f45b40176c8c62cacde09f863acce45cfb2fa0f44564afa0dbfac4017753e_thumb.jpeg')
professorx = User(first_name='Charles', last_name='Xaviar', profile_img='https://screenrant.com/wp-content/uploads/professor-x.jpg')

# Add posts
p1 = Post(title='Jean Grey Bio', content='Jean Grey has telepathic and telekinetic powers. She is a mutant and is part of the x-men', user_id=1)
p2 = Post(title='Scott Summers Bio', content='Scott Summers emits concussive blasts from his eyes. He is a mutant and is part of the x-men. ', user_id=2)
p3 = Post(title='Charles Xavier Bio', content='Charles Xavier has telepathic powers. He is a mutant and the founder of the x-men.', user_id=3)

# Add new objects to session, so they'll persist
db.session.add_all([darkphoenix, cyclops, professorx])

# Commit--otherwise, this never gets saved!
db.session.commit()

db.session.add_all([p1, p2, p3])

db.session.commit()

# Add tags
t1 = Tag(name='telekinesis')

t2 = Tag(name='telepathic')

t3 = Tag(name='concussive')

t4 = Tag(name='mutant')

t5 = Tag(name='x-men')



db.session.add_all([t1, t2, t3, t4, t5])

db.session.commit()