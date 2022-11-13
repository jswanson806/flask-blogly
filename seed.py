"""Seed file to make sample data for users db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
darkphoenix = User(first_name='Jean', last_name="Grey")
cyclops = User(first_name='Scott', last_name="Summers")
professorx = User(first_name='Charles', last_name="Xaviar")

# Add new objects to session, so they'll persist
db.session.add(darkphoenix)
db.session.add(cyclops)
db.session.add(professorx)

# Commit--otherwise, this never gets saved!
db.session.commit()