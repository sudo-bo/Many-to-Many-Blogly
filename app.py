"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.debug = False # can change when needed

app.config['SECRET_KEY'] = 'development key'  # Needed for Flask sessions and debug toolbar
toolbar = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()

@app.route("/")
def root():
    return redirect("/users")

@app.route("/users")
def users_page():
    all_users = User.get_users()
    return render_template("users.html", users=all_users)

@app.route("/users/<int:id>")
def user_info(id):
    user = User.find_user(id) # returns a 404 error if not found
    return render_template("user-detail.html", user=user)

@app.route("/users/new")
def add_user():
    return render_template("add-user.html")

@app.route("/users/new", methods=['POST'])
def new_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form.get('image_url')

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url if image_url else None)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:id>/edit")
def edit_user(id):
    user = User.find_user(id) # returns a 404 error if not found
    return render_template("edit-user.html", user=user)

@app.route("/users/<int:id>/edit", methods=['POST'])
def edit_user_post_request(id):
    user = User.find_user(id) # returns a 404 error if not found

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form.get('image_url', user.image_url)  # Use existing image_url if not provided

    db.session.commit()

    return render_template("user-detail.html", user=user)

@app.route("/users/<int:id>/delete", methods=['POST'])
def delete_user(id):
    user = User.find_user(id) # returns a 404 error if not found
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")