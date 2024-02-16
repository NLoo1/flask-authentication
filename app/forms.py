from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, FloatField, TextAreaField, validators, PasswordField
from wtforms.validators import InputRequired, Optional, Length

class AddUserForm(FlaskForm):
    """Form for adding users."""

    username= StringField("Username",
                      validators=[InputRequired(),Length(max=20)])
    password= PasswordField("Password",
                      validators=[InputRequired()])
    email= StringField("Email",
                      validators=[InputRequired(), Length(max=50)])
    first_name= StringField("First Name",
                      validators=[InputRequired(), Length(max=30)])
    last_name= StringField("Last Name",
                      validators=[InputRequired(), Length(max=30)])
    
class LoginUserForm(FlaskForm):
    username= StringField("Username",
                      validators=[InputRequired(),Length(max=20)])
    password= PasswordField("Password",
                      validators=[InputRequired()])
    
class AddFeedbackForm(FlaskForm):
    title = StringField('Title',
                        validators=[InputRequired(),Length(max=100)])
    content = StringField('Content',
                          validators=[InputRequired()])