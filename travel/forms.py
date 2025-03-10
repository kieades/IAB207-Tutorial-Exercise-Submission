from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, Email, EqualTo

ALLOWED_FILE = {'PNG', 'JPG', 'png', 'jpg'}



class DestinationForm(FlaskForm):
    name = StringField('Country', validators=[InputRequired(), Length(min=3)])
    # adding two validators, one to ensure input is entered and other to check if the 
    # description meets the length requirements
    description = TextAreaField('Description', validators = [InputRequired()])
    image = FileField('Destination Image', validators=[FileRequired(message='Image cannot be empty'), FileAllowed(ALLOWED_FILE, message='Only PNG or JPG files')])
    currency = StringField('Currency', validators=[InputRequired()])
    submit = SubmitField("Create")
    
# User login
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

# User register
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = EmailField("Email Address", validators=[Email("Please enter a valid email")])
    
    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    # submit button
    submit = SubmitField("Register")

class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')