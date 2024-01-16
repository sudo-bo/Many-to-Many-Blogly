from unittest import TestCase

from models import User, db
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False


app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

with app.app_context():
    db.drop_all()
    db.create_all()

class UserViewFunctions(TestCase):
    """Test view functions for app.py (for Users)"""

    def setUp(self):
        with app.app_context():
            User.query.delete()
            mike = User(first_name = "Michael", last_name = "Jordan")
            db.session.add(mike)
            db.session.commit()
            self.mike_id = mike.id # for a route that requires a user id

    def tearDown(self):
        with app.app_context():
            db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jordan', html)

    def test_create_users(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Create a user</h2>', html)

    def test_add_user(self):
        with app.test_client() as client:
            response = {"first_name": "Mr", "last_name": "Sandman"}
            resp = client.post("/users/new", data = response, follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Mr Sandman', html)
    
    def test_user_picture(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.mike_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('lumiere-a.akamaihd.net', html) # checks if default picture is in page
            