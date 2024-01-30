from models import db, User, Blog_Post
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()



  
def create_sample_user():
    # Insert sample user data
    existing_user = User.query.filter_by(email='sandra.colorado@example.com').first()

    if not existing_user:
        # Create a new user if not exists
        hashed_password = bcrypt.generate_password_hash("user_password").decode("utf-8")
        user = User(first_name="Sandra", last_name="Colorado", email="sandra.colorado@example.com", password=hashed_password, subscribe=True, admin_user=True)
        db.session.add(user)
        db.session.commit()

def create_blog_post():
    #Insert sample blog post
    existing_blog_post = Blog_Post.query.filter_by(title="La Isla Del Encanto").first()
    if not existing_blog_post:
        blog_post = Blog_Post(title="La Isla Del Encanto", 
                            content="The Spanish word Encanto has been brought to the attention of many non-Spanish speaking people with the recent release of the Disney movie of the same name which takes place in the country of Columbia. But did you know that Puerto Rico is known as “La Isla del Encanto” which in English translates to “The Island of Enchantment”. And after visiting Puerto Rico, I could not agree more with this. The island of Puerto Rico is located in the Caribbean and is a territory of The United States of America. This makes it a very easy destination for US visitors as passports are not required. But this beautiful island is more than just tropical beaches and relaxation. It’s full of history, culture and outdoor activities.", 
                            image_url="https://www.planetware.com/wpimages/2020/01/puerto-rico-in-pictures-beautiful-places-to-photograph-san-juan.jpg", 
                            user_id = User.query.filter_by(email="sandra.colorado@example.com").first().id)
        db.session.add(blog_post)
        db.session.commit()


