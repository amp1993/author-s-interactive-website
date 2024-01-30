from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__='users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique = True)
    password = db.Column(db.Text, nullable = False)
    subscribe = db.Column(db.Boolean, nullable= False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    admin_user = db.relationship('Admin_User', back_populates='user')


    def serialize_user(self):
        
        return {
                'id' : self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
                'password': self.password,
            }

    
    @classmethod
    def signup(cls, first_name, last_name, email, password, subscribe):
        """Sign up user.

        Hashes password and adds user to system.
        """
        if email is None or len(password) < 6:
            return None
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            first_name = first_name,
            last_name = last_name,
            email= email,
            password= hashed_pwd,
            subscribe = subscribe
            )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, email, password):


        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    
    @property
    def is_admin(self):
        return Admin_User.query.filter_by(user_id=self.id).first() is not None



class Blog_Post(db.Model):

    __tablename__='blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable = False)
    timestamp = db.Column(db.DateTime, nullable= False, default=datetime.utcnow())
    image_url = db.Column(db.Text, nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable = False)
    user = db.relationship('User')



    
class Admin_User(db.Model):

    __tablename__='admin_users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable = False)
    user = db.relationship('User', back_populates='admin_user')

  
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)