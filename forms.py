from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from .models import User, Post, LoginHistory

class RegistrationForm(FlaskForm):
    username = StringField('Username', id='uname',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', id='pword', validators=[DataRequired()])
    twofactor = StringField('Two Factor', id='2fa', validators=[DataRequired(), Length(10,11)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', id='uname',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', id='pword', validators=[DataRequired()])
    twofactor = StringField('Two Factor', id='2fa', validators=[DataRequired(), Length(10,11)])
    submit = SubmitField('Login')

class HistoryForm(FlaskForm):
    user_id = IntegerField('Enter User ID', id='userquery', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    content = TextAreaField('Enter text to spell check', id='inputtext', validators=[DataRequired()])
    submit = SubmitField('Spell Check')

class AdminQuery(FlaskForm):
    username = StringField('Enter Username', id='userquery', validators=[DataRequired()])
    submit = SubmitField('Submit')



