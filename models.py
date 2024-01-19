"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
def connect_db(app):
    """Connect this database to provided Flask app."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.Text, default="https://lumiere-a.akamaihd.net/v1/images/pooh_baeb7dc6.jpeg?region=410,0,1229,1229")

    #  to populate users.html
    @classmethod
    def get_users(cls):
        return cls.query.all()
    
    # to provide info for user-detail.html
    @classmethod
    def find_user(cls, id):
        return cls.query.get_or_404(id)

class Post(db.Model):
    """Posts."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='posts')
    
    # direct connection to post/tag connector table
    tag_relations = db.relationship('PostTag', backref='post')
    # through connection to tag table
    tags = db.relationship('Tag', secondary='post_tag', backref='posts')
    
    @classmethod
    def find_post(cls, id):
        return cls.query.get_or_404(id)

class PostTag(db.Model):
    """Many to Many Post-Tag Relationship."""

    __tablename__ = 'post_tag'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    

    @classmethod
    def find_relationship(cls, id):
        return cls.query.get_or_404(id)
    
class Tag(db.Model):
    """Tags."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    # direct connection to post/tag connector table
    post_relations = db.relationship('PostTag', backref='tag')

    @classmethod
    def find_tag(cls, id):
        return cls.query.get_or_404(id)
