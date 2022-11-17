"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post


app = Flask(__name__)
    

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home_page():
    
    return redirect('/users')

@app.route('/users')
def list_users():
    """Show the list of users."""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def show_add_users_form():
    """Show the new user form."""
    return render_template('new.html')

@app.route('/users', methods=["POST"])
def create_user():
    """Add a new user to the db from the form input."""
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    profile_img = request.form["profile-img"]

    new_user = User(first_name=first_name, last_name=last_name, profile_img=profile_img)

    db.session.add(new_user)

    db.session.commit()

    return redirect("/")

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """Show user details."""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('details.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    """Show edit user form."""
    user = User.query.get_or_404(user_id)

    return render_template('edit-user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Update user in the db from the form input."""

    user = User.query.get_or_404(user_id)

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    profile_img = request.form["profile-img"]

    user.id = user_id
    user.first_name = first_name
    user.last_name = last_name
    user.profile_img = profile_img

    db.session.commit()

    return redirect("/")


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete user from the db."""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)

    db.session.commit()

    return redirect("/")

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Show the form to add a post."""
    user = User.query.get_or_404(user_id)

    return render_template('posts.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_new_post(user_id):
    """Add new post to the db from the form input."""

    user = User.query.get_or_404(user_id)
    

    title = request.form["post-title"]
    content = request.form["post-content"]


    new_post = Post(title=title, content=content, user_id=user.id)

    db.session.add(new_post)

    db.session.commit()

    return redirect(f'/users/{user.id}')

@app.route('/posts/<int:post_id>')
def show_specific_post(post_id):
    """Show post content."""
    post = Post.query.get_or_404(post_id)
    return render_template('post-content.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show edit post form."""
    post = Post.query.get_or_404(post_id)

    return render_template('edit-post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Update post in the db from the form input."""

    post = Post.query.get_or_404(post_id)

    title = request.form["post-title"]
    content = request.form["post-content"]

    post.id = post_id
    post.title = title
    post.content = content
    

    db.session.commit()

    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Delete post from the db."""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)

    db.session.commit()

    return redirect(f'/users/{post.user_id}')