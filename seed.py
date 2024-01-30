from app import app
from models import db, User, Admin_User, Blog_Post
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

with app.app_context():
    # Drop and recreate the database tables
    db.drop_all()
    db.create_all()

    # Insert sample user data
    hashed_password = bcrypt.generate_password_hash("user_password").decode("utf-8")
    user = User(first_name="Sandra", last_name="Colorado", email="sandra.colorado@example.com", password=hashed_password, subscribe=True)
    db.session.add(user)
    db.session.commit()

    # Make the user an admin
    admin_user = Admin_User(user=user)
    db.session.add(admin_user)
    db.session.commit()

    #Insert sample blog post
    blog_post = Blog_Post(title="La Isla Del Encanto", content="The Spanish word Encanto has been brought to the attention of many non-Spanish speaking people with the recent release of the Disney movie of the same name which takes place in the country of Columbia. But did you know that Puerto Rico is known as “La Isla del Encanto” which in English translates to “The Island of Enchantment”. And after visiting Puerto Rico, I could not agree more with this. The island of Puerto Rico is located in the Caribbean and is a territory of The United States of America. This makes it a very easy destination for US visitors as passports are not required. But this beautiful island is more than just tropical beaches and relaxation. It’s full of history, culture and outdoor activities.", image_url="https://www.planetware.com/wpimages/2020/01/puerto-rico-in-pictures-beautiful-places-to-photograph-san-juan.jpg", user_id = user.id)
    db.session.add(blog_post)
    db.session.commit()

   