from flask import Flask, render_template, request, redirect, session, g, flash, url_for
from sqlalchemy.exc import IntegrityError
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv

from forms import SignUpForm, LoginForm, CreateBlogPost,EditBlogPost, CharacterSelectionForm
from models import User, Blog_Post, init_db, db
import openai
from openai.error import OpenAIError
from datetime import datetime, timedelta
from seed import create_blog_post, create_sample_user

import os

#Load variables from .env


app = Flask(__name__)

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CURR_USER_KEY = "curr_user"

# Fetch story to be used for API
with open("SamSatito.txt", "r", encoding="utf-8") as file:
    story = file.read()

# Initialize the database
init_db(app)

with app.app_context():
    create_sample_user()
    create_blog_post()


def init_conversation():
    if 'conversation' not in session:
        session['conversation'] = []






####################### Index Route ####################################

@app.route('/', methods=['GET'])
def index():

    blog_posts = Blog_Post.query.all()
    
    return render_template('homepage.html', blog_posts=blog_posts)

########################### User signup/login/logout ##################################################

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        
def before_first_request():
    with app.app_context():
        init_conversation()


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup."""
    try: 
        form = SignUpForm()

        if form.validate_on_submit():
            try:
                user = User.signup(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=form.password.data,
                    subscribe=form.subscribe.data
                )
                db.session.commit()
        

            except IntegrityError:
                flash("Email is associated with an account. Log In instead", 'danger')
                return redirect(url_for('login'))  

            do_login(user)

            return redirect(url_for('index'))
        

        return render_template('login/signup.html', form=form)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        return redirect(url_for('index'))


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""
    try:

        form = LoginForm()

        if form.validate_on_submit():
            user = User.authenticate(form.email.data, form.password.data)

            if user:
                do_login(user)
                return redirect(url_for('index'))  
    

        return render_template('/login/login.html', form=form)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    """Handle logout of user."""
    try:
        if g.user:
            do_logout()
            flash(f"You have successfully logged out!")

            
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        return redirect(url_for('index'))


############################ Blog Post Routes ################################################

@app.route('/blog', methods=["GET"])
def show_all_blog_posts():
    try:
        blog_posts = Blog_Post.query.all()
        user = g.user
        return render_template('/blog/blog_posts.html', blog_posts=blog_posts,  user=user)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        return redirect(url_for('index'))
    
@app.route('/blog/<int:blog_post_id>', methods=["GET"])
def show_selected_blog_post(blog_post_id):
    try:
        blog_post = Blog_Post.query.get_or_404(blog_post_id)
        user = g.user

        return render_template('/blog/post_content.html', blog_post=blog_post, user = user)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        return redirect(url_for('index'))

@app.route('/blog/new', methods=["GET", "POST"])
def create_blog_post():
    try:
    # Check if the user is logged in and is an admin
        if g.user is None or not g.user.admin_user:
            flash("User unauthorized.", "danger")
            return redirect("/")

        form = CreateBlogPost()

        if form.validate_on_submit():    
            blog_post = Blog_Post(
                title=form.title.data,
                content=form.content.data,
                image_url=form.image_url.data,
                user_id=g.user.id  # Set the user_id for the blog post to the current user's id
            )
            db.session.add(blog_post)
            db.session.commit()

            return redirect(url_for('show_all_blog_posts'))

        
        return render_template('/blog/new_form.html', form=form)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        return redirect(url_for('index'))

@app.route('/blog/<int:blog_post_id>/edit', methods=["GET", "POST"])
def edit_blog_post(blog_post_id):

    try:

    # Check if the user is logged in and is an admin
        if g.user is None or not g.user.admin_user:
            flash("User unauthorized.", "danger")
            return redirect("/")

        blog_post = Blog_Post.query.get_or_404(blog_post_id)
        user = g.user

        form = EditBlogPost(obj=blog_post)

        if form.validate_on_submit():
            blog_post.title = form.title.data
            blog_post.content=form.content.data
            blog_post.image_url = form.image_url.data
            
            db.session.commit()

            flash('Post has been updated','success')
            return redirect(url_for('show_selected_blog_post', blog_post_id=blog_post.id))


        
        return render_template('/blog/edit_form.html', form=form, blog_post=blog_post, user=user)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        return redirect(url_for('index'))


@app.route('/blog/<int:blog_post_id>/delete', methods=["POST"])
def delete_blog_post(blog_post_id):
    try:
        # Check if the user is logged in and is an admin
        if g.user is None or not g.user.admin_user:
            flash("User unauthorized.", "danger")
            return redirect("/")
        
        blog_post = Blog_Post.query.get_or_404(blog_post_id)


        db.session.delete(blog_post)
        db.session.commit()

        return redirect(url_for('show_all_blog_posts'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        return redirect(url_for('index'))




################################# Chatbot Routes##############################################


@app.route('/chat', methods=['GET', 'POST'])
def select_character():

    try:
        if not g.user:
            flash("Please log in to access the chat.", "danger")
            return redirect("/login")

        form = CharacterSelectionForm()

    

        if form.validate_on_submit():
            # Store the selected character in the session
            session['selected_character'] = form.character_choice.data
            return redirect(url_for('chat', character=session['selected_character']))

        return render_template('/chatbot/select_character.html', form=form)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        return redirect(url_for('index'))


@app.route("/chat/<character>", methods=["GET", "POST"])
def chat(character):

    try:
        # Ensure character is a string
        character = str(character)
        user_input = request.form.get("user_input")

        assistant_reply=''

        if user_input is not None:

            if character == 'Margie':
                prompt = [
                    {"role": "system", "content":  f"You are Margie, the compassionate and kind-hearted woman from the {story}. Respond to {user_input} with patience and empathy."},
                    {"role": "user", "content": str(user_input)},
                    {"role": "assistant", "content": str(user_input)},
                ]
            elif character == 'Sam':
                prompt = [
                    {"role": "system", "content": f"You are Sam, the lovable and playful dog from the {story}. Respond to {user_input} in a playful and endearing manner."},
                    {"role": "user", "content": str(user_input)},
                    {"role": "assistant", "content": str(user_input)},
                ]
            # Retrieve the conversation history from the session
            conversation = session.get('conversation', [])

            # Append the user's input to the conversation
            conversation.append({"role": "user", "content": user_input})

            # Use OpenAI API to generate a completion
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-1106",
                messages=prompt,
                max_tokens=150,
                temperature=0.2
            )

            # Extract the assistant's reply
            assistant_reply = response['choices'][0]['message']['content']

            # Append the assistant's reply to the conversation
            conversation.append({"role": "assistant", "content": assistant_reply})

            # Update the conversation history in the session
            session['conversation'] = conversation

        

        return render_template("/chatbot/chat.html", user_input=user_input, assistant_reply=assistant_reply, character=character)

    except OpenAIError as api_error:
            # Handle OpenAI API errors
            if 'rate limit' in str(api_error).lower():
                flash("API rate limit exceeded. Please try again later.", 'danger')
            else:
                flash(f"OpenAI API error: {str(api_error)}", 'danger')

            return redirect(url_for('index'))

    except Exception as e:
            # Handle other unexpected errors
            flash(f"An error occurred: {str(e)}", 'danger')
            return redirect(url_for('index'))

############################# Books Landing Pages ##################################################


@app.route('/books/sam-satito', methods=["GET"])
def get_sam_satito_book_content():

    return render_template('/books/sam-satito.html')


@app.route('/books/el-dia-que-trascendi-los-limites-de-la-cordura', methods=["GET"])
def get_limites_de_la_cordura_book_content():

    return render_template('/books/limites-de-la-cordura.html')


@app.route('/books/siempre_en_viernes', methods=["GET"])
def get_simpre_en_viernes_book_content():

    return render_template('/books/siempre-en-viernes.html')


@app.route('/books/de-7-a-9', methods=["GET"])
def get_7_a_9_book_content():

    return render_template('/books/de-7-a-9.html')


############################### About Landing Page ##################################################

@app.route('/about', methods=["GET"])
def about():

    return render_template('about.html')
     
############################### Admin Dashboard Landing Page ############################################

@app.route('/admin', methods=["GET"])
def show_admin_report():
     
    try:
        if g.user is None or not g.user.admin_user:
            flash("User unauthorized.", "danger")
            return redirect("/")
        
        else:
        # Query the total number of users and blog posts
            total_users = User.query.count()
            total_blog_posts = Blog_Post.query.count()

            # Query new users (signed up in the last week)
            last_week = datetime.utcnow() - timedelta(days=7)
            new_users = User.query.filter(User.timestamp >= last_week).all()

            # Render the template with the data
            return render_template('admin_dashboard.html', total_users=total_users, total_blog_posts=total_blog_posts, new_users=new_users)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
