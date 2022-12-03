from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Email

class Login(FlaskForm):
    email = StringField('email', validators=[Email(), InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
    submit = SubmitField('Login', render_kw={'class': 'btn waves-effect waves-light white-text'})