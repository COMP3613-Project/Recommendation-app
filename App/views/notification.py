from flask import Blueprint, render_template, jsonify, request, send_from_directory, Response, redirect, url_for
from flask_jwt import jwt_required, current_identity
from flask_login import  LoginManager, current_user, login_user, login_required
from App.forms import Recommendation

from App.controllers import (
    send_notification,
    get_all_notifs_json,
    get_staff,
    get_user_notif,
    send_recommendation,
    get_request,
    get_notif_by_request,
    delete_notification,
    approve_request
)

notification_views = Blueprint('notification_views', __name__, template_folder='../templates')

# VIEW NOTIFICATION
@notification_views.route('/notifications/<notifID>', methods=['GET'])
#@jwt_required()
def view_notif(notifID):
    staff = get_staff(current_user.id)
    if staff:
        if not staff.notificationFeed:
            return Response({"no notifications found for this user"}, status=404)
        notif = get_user_notif(current_user.id, notifID)
        if notif:
            request = get_request(notif.requestID)
            return render_template('specificNotification.html',request = request)
        return Response({"notification with id " + notifID + " not found"}, status=404)
    return Response({"students cannot perform this action"}, status=401)


# APPROVE REQUEST
@notification_views.route('/request/<notifID>/approve', methods=['GET'])
#@jwt_required()
def approverequest(notifID):
    form = Recommendation()
    request = get_request(notifID)
    return render_template('sendRecommendation.html', form = form, request = request)

@notification_views.route('/request/<notifID>/approve', methods=['POST'])
#@jwt_required()
def approve_request_action(notifID):
    form = Recommendation()
    if form.validate_on_submit(): # respond to form submission
      data = request.form
      studrequest = get_request(notifID)
      if studrequest:
         send_recommendation(studrequest.staffID, studrequest.studentID, data['recomText'])
         approve_request(notifID, "approved")
         staff = get_staff(current_user.id)
         notif = get_notif_by_request(studrequest.requestID)
         if notif:
            delete_notification(notif)
         return redirect(url_for('index_views.home'))
    else:
        return Response(form.errors)

@notification_views.route('/request/<notifID>/reject', methods=['GET','DELETE'])
#@jwt_required()
def reject_request_action(notifID):
    studrequest = get_request(notifID)
    if studrequest:
        approve_request(notifID, "rejected") 
        staff = get_staff(current_user.id)
        notif = get_notif_by_request(studrequest.requestID)
        if notif:
            delete_notification(notif)
        return redirect(url_for('index_views.home'))
    else:
        return redirect(url_for('index_views.home'))
