from App.models import Recommendation, Student, Notification, Staff, Request
from App.database import db
from sqlalchemy.exc import IntegrityError
from App.controllers import send_notification, get_staff, get_student

def create_request(staffID, title, studentID, requestText):
    newrequest = Request(staffID=staffID, title = title, studentID=studentID, requestText=requestText)
    return newrequest

def send_request(staffID, title, studentID, requestText):
    staff = get_staff(staffID)
    stud = get_student(studentID)
    
    if(staff):
        if(stud):
            newrequest = create_request(staffID, title, studentID, requestText)
            try:
                db.session.add(newrequest)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return None
            print(newrequest.toJSON())
            send_notification(newrequest.requestID,title,staffID)
    
def get_request(requestID):
    return Request.query.filter_by(requestID = requestID).first()

def get_student_requests(studentID):
    return Request.query.filter_by(studentID = studentID).all()

def get_all_requests():
    return Request.query.all()

def get_all_accepted_requests(staffID):
    return Request.query.filter_by(staffID=staffID, status = "approved").all()

def get_all_rejected_requests(staffID):
    return Request.query.filter_by(staffID=staffID, status = "rejected").all()

def get_all_requests_json():
    requests = get_all_requests()
    if not requests:
        return None
    requests = [Request.toJSON() for Request in requests]
    return requests
    
def change_status(request, status):
    if request:
        request.status = status
    return request

def approve_request(requestID, status):
    request = get_request(requestID)
    request = change_status(request, status)
    if request:
        try:
            db.session.add(request)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
    return request