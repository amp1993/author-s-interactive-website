from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

def init_db(app):
    db.init_app(app)
    bcrypt.init_app(app)
    with app.app_context():
        db.create_all()

class User(db.Model):
    __tablename__='users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique = True)
    password = db.Column(db.Text, nullable = False)
    subscribe = db.Column(db.Boolean, nullable= False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    admin_user = db.Column(db.Boolean, default=False)

    
    @classmethod
    def signup(cls, first_name, last_name, email, password, subscribe, admin_user = False):
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
            subscribe = subscribe,
            admin_user=admin_user
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
    
   



class Blog_Post(db.Model):

    __tablename__='blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable = False)
    timestamp = db.Column(db.DateTime, nullable= False, default=datetime.utcnow())
    image_url = db.Column(db.Text, nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable = False)
    user = db.relationship('User')




  
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)