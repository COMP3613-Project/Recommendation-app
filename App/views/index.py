from flask import Blueprint, redirect, render_template, request, send_from_directory
from App.forms import Login

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    form = Login()
    return render_template('login.html', form=form)

#user submits the login form
@index_views.route('/login', methods=['POST'])
def loginAction():
  form = LogIn()
  if form.validate_on_submit(): # respond to form submission
      data = request.form
      user = User.query.filter_by(email = data['email']).first()
      if user and user.check_password(data['password']): # check credentials
        flash('Logged in successfully.') # send message to next page
        login_user(user) # login the user
        return render_template('users.html')
  flash('Invalid credentials')
  return redirect(url_for('index'))
