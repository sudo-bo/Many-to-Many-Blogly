"""Seed file to make sample data for blogly db"""

from models import User, Post, Tag, db
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()
    User.query.delete()
    Tag.query.delete()
    Post.query.delete()

    # some us presidents/political figures 
    adam = User(first_name = "Adam", last_name = "Samuel")
    benjamin = User(first_name = "Benjamin", last_name = "Franklin")
    george = User(first_name = "George", last_name = "Washington")

    db.session.add_all([adam, benjamin, george])
    db.session.commit()

    # initial tags
    tag1 = Tag(name = "moody")
    tag2 = Tag(name = "clouded")
    tag3 = Tag(name = "lost")

    db.session.add_all([tag1, tag2, tag3])
    db.session.commit()

    # intial posts for the website
    post1 = Post(title = "Brother", content = "Where is he", user_id = adam.id)
    post2 = Post(title = "America", content = "I wonder where it'll be in a hundred years", user_id = adam.id)
    post3 = Post(title = "Thoughts on money", content = "Too many", user_id = benjamin.id)

    post1.tags.append(tag1)
    post1.tags.append(tag2)
    post2.tags.append(tag3)

    db.session.add_all([post1, post2, post3])
    db.session.commit()