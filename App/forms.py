from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import InputRequired, EqualTo, Email

class Login(FlaskForm):
    email = StringField('email', validators=[Email(), InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired()])
    submit = SubmitField('Login', render_kw={'class': 'btn waves-effect waves-light white-text'})

class SignUp(FlaskForm):
    firstName = StringField('First Name', validators=[InputRequired()])
    lastName = StringField('Last Name', validators=[InputRequired()])
    email = StringField('email', validators=[Email(), InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired()])#, EqualTo('confirm', message='Passwords must match')])
    #confirm  = PasswordField('Repeat Password')
    usertype = RadioField('User Type', choices=[('staff','staff'),('student','student')])
    submit = SubmitField('Sign Up', render_kw={'class': 'btn waves-effect waves-light white-text'})

class Request(FlaskForm):
    staffName = StringField('Staff name', validators=[InputRequired()],render_kw={"placeholder":"Enter staff member name"})
    title = StringField('Request subject', validators=[InputRequired()],render_kw={"placeholder":"Enter Request subject"})
    text = StringField('Request Text', validators=[InputRequired()],render_kw={"placeholder":"Request Text", "rows":"10", "cols":"30" })
    submit = SubmitField('Submit', render_kw={'class': 'btn waves-effect waves-light white-text'})

class Recommendation(FlaskForm):
    recomText = StringField('Recommendation Tex',validators=[InputRequired()],render_kw={"placeholder":"Enter recommendation text"})
    submit = SubmitField('Submit', render_kw={'class': 'btn waves-effect waves-light white-text'})