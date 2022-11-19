"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, PostTag, Tag


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
    tags = Tag.query.all()
    return render_template('posts.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_new_post(user_id):
    """Add new post to the db from the form input."""

    user = User.query.get_or_404(user_id)
    

    title = request.form["post-title"]
    content = request.form["post-content"]

    tags = request.form.getlist("tag-name")

    new_post = Post(title=title, content=content, user_id=user.id)

    db.session.add(new_post)

    db.session.commit()

    for tag in tags:
        post_tag = db.session.query(Tag).filter_by(name=f'{tag}').all()
        new_post.tags.append(post_tag[0])

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
    tags = Tag.query.all()
    return render_template('edit-post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Update post in the db from the form input."""

    post = Post.query.get_or_404(post_id)

    title = request.form["post-title"]
    content = request.form["post-content"]

    tags = request.form.getlist("tag-name")

    post.id = post_id
    post.title = title
    post.content = content
    
    post.tags[:] = []

    db.session.commit()

    for tag in tags:
        post_tag = db.session.query(Tag).filter_by(name=f'{tag}').all()
        post.tags.append(post_tag[0])

    db.session.commit()

    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Delete post from the db."""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)

    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/tags')
def show_tags():
    """List all tags in the db."""
    tags = Tag.query.all()

    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """Show details of specific tag."""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag-details.html', tag=tag)

@app.route('/tags/new')
def show_add_tag_form():
    """Show the form to add a new tag."""
    return render_template('new-tag.html')

@app.route('/tags/new', methods=["POST"])
def add_new_tag():
    """Add new tag to the db from the form input."""

    name = request.form["tag-name"]

    new_tag = Tag(name=name)

    db.session.add(new_tag)

    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """Show edit tag form."""
    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit-tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    """Update tag in the db from the form input."""

    tag = Tag.query.get_or_404(tag_id)

    name = request.form["tag-name"]

    tag.id = tag_id
    tag.name = name
    
    db.session.commit()

    return redirect(f'/tags/{tag.id}')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    """Delete tag from the db."""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)

    db.session.commit()

    return redirect(f'/tags')