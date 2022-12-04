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



# Routes for testing purposes
# check identity of current user
@user_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
    return jsonify({'message': f"id : {current_identity.id}, email: {current_identity.email}, userType: {current_identity.userType}"})

# View all Users
@user_views.route('/view/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

# JSON View all Users
@user_views.route('/users')
def client_app():
    users = get_all_users_json()
    return jsonify(users)

# STATIC View all Users
@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')
