from flask import Blueprint, redirect, render_template, request, send_from_directory, flash, Response, url_for
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
    get_request,
    get_all_requests,
    get_student_requests,
    send_request,
    get_staff_by_name,
    get_student_recommendations,
    get_staff,
    get_recommendation,
    get_student,
    logout_user,
    get_user
)

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def login():
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
        return redirect(url_for('index_views.home'))
      else:
        Response("Invalid login credentials")
        form = Login()
        return render_template('login.html', form=form)
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
  return render_template('makeRequest.html',form = form, firstName = current_user.firstName)

@index_views.route('/submit/request', methods = ['POST'])
def submitrequest():
  form = Request()
  if form.validate_on_submit():
    data = request.form
    staffname = data['staffName'].split()
    staff = get_staff_by_name(staffname[0],staffname[1])
    if staff:
      student=get_student(current_user.id)
      send_request(staff.id,data['title'],student.id,data['text'])
      return redirect(url_for('index_views.home'))
    else :
      flash("Staff member does not exist")
      return redirect(url_for('index_views.makerequest'))
  else:
    return Response(form.errors)

@index_views.route("/request/<requestID>/view", methods=['GET'])
def view_student_request(requestID):
    print(requestID)
    request = get_request(requestID)
    return render_template('viewRequest.html',request=request, firstName=current_user.firstName)

@index_views.route('/logout', methods = ['GET'])
def logout():
    logout_user()
    return redirect(url_for('index_views.login'))

@index_views.route('/home',methods = ['GET'])
def home():
  user = get_user(current_user.id)
  if user:
    if user.userType == "student" :
          requests = get_student_requests(current_user.id)
          recoms = get_student_recommendations(current_user.id)
          return render_template('StudentHome.html',firstName=user.firstName, requests = requests, recoms = recoms)
    else:
          staff = get_staff(current_user.id)
          notifications = staff.notificationFeed
          return render_template('staffHome.html',notifications = notifications, firstName = staff.firstName, staffID = user.id)
  else:
    return Response("We not innit")




  
