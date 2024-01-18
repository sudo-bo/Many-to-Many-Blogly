"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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


#  part 2 - adding posts
#
#

@app.route('/users/<int:id>/posts/new')
def add_post_page(id):
    user = User.find_user(id) 
    return render_template("add-post.html", user=user)

@app.route('/users/<int:id>/posts/new', methods = ['POST'])
def add_post(id):
    user = User.find_user(id) # returns a 404 error if not found
    post_title = request.form['title']
    post_content = request.form['content']

    new_post = Post(title = post_title, content = post_content, user_id = user.id)
    db.session.add(new_post)
    db.session.commit()

    return render_template("user-detail.html", user=user)

@app.route('/posts/<int:id>')
def show_post(id):
    post = Post.find_post(id) # returns a 404 error if not found
    return render_template("post-detail.html", post=post)

@app.route('/posts/<int:id>/edit')
def edit_post_page(id):
    post = Post.find_post(id)
    return render_template("edit-post.html", post=post)


@app.route('/posts/<int:id>/edit', methods = ['POST'])
def edit_post(id):
    post = Post.find_post(id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()

    return redirect(f'/posts/{id}')

@app.route('/posts/<int:id>/delete', methods = ['POST'])
def delete_post(id):
    post = Post.find_post(id) # returns a 404 error if not found
    user_id = post.user.id
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")
