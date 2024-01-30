import unittest
import os
from flask import session, url_for
from models import User, Blog_Post, Admin_User



from app import app, db, CURR_USER_KEY 


app.app_context().push()

with app.app_context():
    db.create_all()

app.config['WTF_CSRF_ENABLED'] = False



class UserViewTestCase(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        os.environ['DATABASE_URL'] = "postgresql://test-authors_website_db"

        #Start a transaction
        db.session.begin()

        User.query.delete()

        self.client = app.test_client()


        self.testuser = User.signup(
            first_name="test",
            last_name='user',
            email="test@test.com",
            password="testuser",
            subscribe=True
        )
        self.admin_user = Admin_User(user=self.testuser)

        db.session.add(self.testuser)
        db.session.add(self.admin_user)
        db.session.commit()

        self.testblog = Blog_Post(
            title='test title',
            content='test content here',
            image_url='https://i.pinimg.com/564x/ae/55/56/ae5556018cc12e7bd3b8a15a118d3921.jpg',
            user_id=self.testuser.id
        )
        db.session.add(self.testblog)

        self.testblog2 = Blog_Post(
            title='second test title',
            content='test content here',
            image_url='https://i.pinimg.com/564x/ae/55/56/ae5556018cc12e7bd3b8a15a118d3921.jpg',
            user_id=self.testuser.id
        )
        db.session.add(self.testblog2)

        # Commit changes after adding all objects
        db.session.commit()

    def tearDown(self):
        #Roll back transactions
        db.session.rollback()



    def test_index_route(self):
        with app.test_request_context():
            response = self.client.get(url_for('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CHATBOT FUN TIME', response.data)

    def test_nav_appears(self):
        with app.test_request_context():
            response = self.client.get(url_for('index'))
        self.assertEqual(response.status_code, 200)

        self.assertIn(b'Sandra Colorado',response.data)
        self.assertIn(b'Books',response.data)
        self.assertIn(b'Blog',response.data)

    def test_nav_fields_appear_conditionally(self):
        # Test that certain fields appear once user logs in
        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = self.testuser.id

        with app.test_request_context():
            response = c.get(url_for('index'))
            self.assertIn(b'Chatbot', response.data)

        # user is logged out
        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = None

        with app.test_request_context():
            response = c.get(url_for('index'))
            self.assertIn(b'Sign In', response.data)

    def test_signup_route(self):
        with app.test_request_context():

            response = self.client.get(url_for('signup'))


            response = self.client.post(url_for('signup'), data={
                'first_name': 'second test',
                'last_name': 'user',
                'email': 'seconduser@test.com',
                'password': 'test users',
                'subscribe': False
            })

            self.assertEqual(response.status_code, 302)


    def test_login_route(self):
        """Test the login route."""
        
        with app.test_request_context():
          response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)

        with app.test_request_context():
         response = self.client.post(url_for('login'), data={
            'email': 'test@test.com',
            'password': 'testuser'
        })

        self.assertEqual(response.status_code, 302)



    def test_logout_route(self):
        """Test the logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 1  

            response = c.get('/logout')
            self.assertEqual(response.status_code, 302) 
            self.assertNotIn(CURR_USER_KEY, session)


    def test_admin_dashboard_access(self):
        #test that admin user is able to access dashboard
        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = self.admin_user.id

        with app.test_request_context():
            response_dashboard_admin_user = c.get(url_for('show_admin_report'))
            self.assertEqual(response_dashboard_admin_user.status_code, 302)


if __name__ == '__main__':
    unittest.main()
