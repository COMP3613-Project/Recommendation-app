from flask import Blueprint, render_template, jsonify, request, send_from_directory, Response
from flask_jwt import jwt_required, current_identity
from flask_login import  LoginManager, current_user, login_user, login_required

from App.controllers import (
    send_recommendation,
    get_all_recommendations_json,
    get_student,
    get_recommendation,
    get_student_reclist_json,
    get_student_recommendations,
    get_student_requests
)

recommendation_views = Blueprint('recommendation_views', __name__, template_folder='../templates')

@recommendation_views.route('/recommendation/<recomID>/view', methods = ['GET'])
def viewrecom(recomID):
    student = get_student(current_user.id)
    recom = get_recommendation(current_user.id,recomID)
    if recom:
      return render_template('viewRecommendation.html', recom = recom, firstName=student.firstName)
    else:
      return redirect(url_for('index_views.home'))
    
