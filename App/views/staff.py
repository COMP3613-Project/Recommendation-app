from flask import Blueprint, render_template, jsonify, request, send_from_directory, Response
from flask_jwt import jwt_required, current_identity

from App.controllers import (
    get_staff, 
    get_all_staff,
    get_all_staff_json,
    get_all_staff_notifs_json,
    get_staff_by_name,
    get_staff_by_firstName,
    get_staff_by_lastName,
    get_staff_feed_json,
    get_all_accepted_requests,
    get_all_rejected_requests
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/staff/<staffID>/requests/accepted', methods=['GET'])
def viewaccepted(staffID):
    staff = get_staff(staffID)
    if staff:
        requests = get_all_accepted_requests(staffID)
        return render_template('staffAcceptedRequest.html', requests = requests, tablehead = "Accepted requests", firstName=staff.firstName)
    else:
        return render_template('staffHome.html')

@staff_views.route('/staff/<staffID>/requests/rejected', methods=['GET'])
def viewrejected(staffID):
    staff = get_staff(staffID)
    if staff:
        requests = get_all_rejected_requests(staffID)
        return render_template('staffAcceptedRequest.html', requests = requests, tablehead = "Rejected Requests", firstName=staff.firstName)
    else:
        return render_template('staffHome.html')

