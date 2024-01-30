import unittest
import os
from flask import session
from models import User, Blog_Post, Admin_User



from app import app, db, CURR_USER_KEY 


app.app_context().push()

with app.app_context():
    db.create_all()

app.config['WTF_CSRF_ENABLED'] = False



class BlogPostModelTestCase(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""

        os.environ['DATABASE_URL'] = "postgresql://test-authors_website_db"

        #Start a transaction
        db.session.begin()
        
        User.query.delete()
        Blog_Post.query.delete()
        Admin_User.query.delete()
        

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


        self.testblog2 = Blog_Post(
            title='second test title',
            content='test content here',
            image_url='https://i.pinimg.com/564x/ae/55/56/ae5556018cc12e7bd3b8a15a118d3921.jpg',
            user_id=self.testuser.id
        )
        db.session.add(self.testblog2)
        db.session.commit()

    def tearDown(self):
        #Roll back transactions
        db.session.rollback()



    def test_add_blog_post(self):
        #Test if blog post is added to database
        blog_post = Blog_Post(
            title='test title',
            content='test content here',
            image_url='https://i.pinimg.com/564x/ae/55/56/ae5556018cc12e7bd3b8a15a118d3921.jpg',
            user_id=self.testuser.id
        )
        db.session.add(blog_post)
        db.session.commit()
        #Check if there are two blog_posts (a blog post was added in setup)
        self.assertEqual(Blog_Post.query.count(), 2)


    def test_delete_blog_post(self):
        #Test if blog post is deleted from database
        blog_post=self.testblog2
        db.session.delete(blog_post)
        db.session.commit()
                            
        self.assertEqual(Blog_Post.query.count(), 0)

    def test_blog_post_relationship(self):
        #Test that blog_post is associated with a admin user
        self.testuser = User.query.get(self.testuser.id)

        blog_post = Blog_Post(
                title='test title',
                content='test content here',
                image_url='https://i.pinimg.com/564x/ae/55/56/ae5556018cc12e7bd3b8a15a118d3921.jpg',
                user_id=self.testuser.id
            )
        db.session.add(blog_post)
        db.session.commit()

        self.assertEqual(blog_post.user, self.testuser)
