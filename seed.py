"""Seed file to make sample data for blogly db"""

from models import User, db
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()
    User.query.delete()

# some us presidents/political figures 
adam = User(first_name = "Adam", last_name = "Samuel")
benjamin = User(first_name = "Benjamin", last_name = "Franklin")
george = User(first_name = "George", last_name = "Washington")

with app.app_context():
    db.session.add(adam)
    db.session.add(benjamin)
    db.session.add(george)
    db.session.commit()