from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email, Length
from flask import url_for

class SignUpForm(FlaskForm):
    """Form for adding users."""

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    subscribe = BooleanField('Subscribe to Newsletter')
    

class LoginForm(FlaskForm):
    """Login form."""

    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])


class CreateBlogPost(FlaskForm):

    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=30)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=10)])
    image_url = StringField('Image URL', validators=[DataRequired()])

class EditBlogPost(FlaskForm):

    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=30)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=10)])
    image_url = StringField('Image URL')

class CharacterSelectionForm(FlaskForm):
    character_choice = RadioField('Select a Character', choices=[
        ('Sam'),
        ('Margie')
    ])

