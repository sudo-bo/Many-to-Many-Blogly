"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

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

