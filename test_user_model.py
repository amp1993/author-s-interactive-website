import unittest
import os
from flask import session
from models import User, Blog_Post, Admin_User


os.environ['DATABASE_URL'] = "postgresql://test-authors_website_db"

from app import app, db, CURR_USER_KEY 


app.app_context().push()

with app.app_context():
    db.create_all()

app.config['WTF_CSRF_ENABLED'] = False



class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        os.environ['DATABASE_URL'] = "postgresql://test-authors_website_db"

        #Start a transaction
        db.session.begin()

        User.query.delete()

        self.client = app.test_client()
        
    def tearDown(self):
        #Roll back transactions
        db.session.rollback()

    def test_user_model(self):
        #Test that user model works
        user = User.signup(
            first_name="test",
            last_name='user',
            email="test@test.com",
            password="testuser",
            subscribe=True
        )
        db.session.commit()

            # Check if user was added to the database
        self.assertEqual(User.query.count(), 1)

    def test_admin_user_relationship_model(self):
        #Test that admin is associated with user model
        user = User.signup(
            first_name="test",
            last_name='user',
            email="test@test.com",
            password="testuser",
            subscribe=True
        )
        db.session.commit()

        admin_user = Admin_User(user=user)
        db.session.add(admin_user)
        db.session.commit()


        self.assertEqual(user, admin_user.user)

    




