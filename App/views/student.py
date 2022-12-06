from flask import Blueprint, render_template, jsonify, request, send_from_directory, Response
from flask_jwt import jwt_required, current_identity

from App.controllers import (
    get_student,
    search_staff,
    get_all_students,
    get_all_students_json,
    get_student_reclist_json
)

student_views = Blueprint('student_views', __name__, template_folder='../templates')    
