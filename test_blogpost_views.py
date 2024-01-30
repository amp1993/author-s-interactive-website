import unittest
import os
from flask import session, url_for
from models import User, Blog_Post, Admin_User



from app import app, db, CURR_USER_KEY 


app.app_context().push()

with app.app_context():
    db.create_all()

app.config['WTF_CSRF_ENABLED'] = False



class BlogPostViewTestCase(unittest.TestCase):

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



    def test_blog_posts_route(self):
        #Test show_all_blog_posts route.
        with app.test_request_context():
            response = self.client.get(url_for('show_all_blog_posts'))        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Blog Posts', response.data)


    def test_show_all_blog_posts(self):
        #Test that blog post appaears
        with app.test_request_context():
            response = self.client.get(url_for('show_all_blog_posts'))     
        self.assertIn(b'<p>test title</p>', response.data)
        self.assertIn(b'<p>second test title</p>', response.data)

        self.assertEqual(response.status_code, 200)

          

    def test_create_blog_post(self):
        #Test that admin user is able to create blog post
        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = self.testuser.id

            response = c.post("/blog/new", data={
                "title": "third test title",
                "content": "test content",
                "image_url": None,
                "user_id": self.testuser.id
            })

            self.assertEqual(response.status_code, 200)

    def test_delete_blog_post_view(self):
        #Test that admin user is able to delete blog post

        blog_post=Blog_Post(title='third test title',
                            content='test content',
                            image_url='static/images/author/sandra-colorado-profile-pic.jpg',
                            user_id=self.testuser.id)
        db.session.add(blog_post)
        db.session.commit()
                            
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id      

        response_delete = c.post(f'/blog/{blog_post.id}/delete', follow_redirects=True)
        self.assertEqual(response_delete.status_code, 200)
