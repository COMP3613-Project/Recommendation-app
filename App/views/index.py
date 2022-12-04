from flask import Blueprint, redirect, render_template, request, send_from_directory, flash, Response
from App.forms import Login, SignUp, Request
from App.models import User, Staff, Student
from flask_jwt import JWT
from flask_jwt import jwt_required, current_identity
from flask_login import  LoginManager, current_user, login_user, login_required
import flask_login

from App.controllers import (
    create_user,
    authenticate,
    login_user,
    get_all_users_json,
    get_all_staff_json,
    get_all_students_json,
    get_all_requests_json,
    search_staff,
    create_notification,
    change_status,
    get_all_notifs_json,
    create_recommendation,
    get_all_recommendations_json,
    create_request,
    get_all_requests,
    send_request,
    get_staff_by_name
)

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    form = Login()
    return render_template('login.html', form=form)

#user submits the login form
@index_views.route('/login', methods=['POST'])
def loginAction():
  form = Login()
  if form.validate_on_submit(): # respond to form submission
      data = request.form
      user = authenticate(data['email'],data['password'])
      if user:
        login_user(user, False) # login the user
        if user.userType == "student" :
          return render_template('StudentHome.html',firstName=user.firstName)
        else:
          return render_template('users.html')
  else : 
    return Response(form.errors)
  #flash('Invalid credentials')
  #return render_template('login.html', form = form)

@index_views.route('/signup', methods=['GET'])
def signup():
  form = SignUp() # create form object
  return render_template('signup.html', form=form) # pass form object to template

@index_views.route('/create/request', methods = ['GET'])
def makerequest():
  form = Request()
  return render_template('makeRequest.html',form = form)

@index_views.route('/submit/request', methods = ['POST'])
def submitrequest():
  form = Request()
  if form.validate_on_submit():
    data = request.form
    staffname = data['staffName'].split()
    staff = get_staff_by_name(staffname[0],staffname[1])
    if staff:
      name = staff.firstName
      
      student=Student.query.filter_by(studentID=current_user.ID).first()
      return Response(student.studentID)
      send_request(staff.staffID,data['title'],student.studentID,data['text'])
    else :
      return Response("WE NOT INNIT")
  else:
    return Response(form.errors)
  
