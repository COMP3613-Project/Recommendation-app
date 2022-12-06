from flask import Blueprint, render_template, jsonify, request, send_from_directory, Response, flash
from flask_jwt import jwt_required, current_identity
from App.database import db
from sqlalchemy.exc import IntegrityError
from App.forms import Login, SignUp

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    get_user,
    user_signup,
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')


# SIGNUP - CREATE ACCOUNT
@user_views.route('/signup', methods=['POST'])
def createAccount():
    
    form = SignUp() 
    
    if form.validate_on_submit():
        data = request.form # get data from form submission
    
        user_signup(data['email'], data['firstName'], data['lastName'], data['usertype'], data['password'])
        form2 = Login()
        return render_template('login.html',form = form2)
    else:
        form2 = SignUp()
        return render_template('signup.html',form = form2) 


