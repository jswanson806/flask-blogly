from unittest import TestCase

from app import app
from models import db, User

# Use test databse and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# dont use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Jean", last_name="Gray")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
    
    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        """Tests users list route."""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jean', html)
    
    def test_show_user_details(self):
        """Tests /users/<int:user_id> page route."""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Jean Gray</h1>', html)

    def test_add_user(self):
        """Tests /users/new route."""
        with app.test_client() as client:
            d = {"first-name": "Scott", "last-name": "Summers", "profile-img": 'https://images.pexels.com/photos/14139354/pexels-photo-14139354.jpeg?auto=compress&cs=tinysrgb&w=600&lazy=load'}
            resp = client.post("/users", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a href="/users/2">Scott Summers</a>', html)

    def test_edit_user_form(self):
        """Tests /users/<int:user_id>/edit route."""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<input type="text" name="first-name" placeholder="first name">', html)