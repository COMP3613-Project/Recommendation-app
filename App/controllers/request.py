from App.models import Recommendation, Student, Notification, Staff, Request
from App.database import db
from sqlalchemy.exc import IntegrityError
from App.controllers import send_notification, get_staff, get_student

def create_request(staffID, studentID, requestText):
    newrequest = Request(staffID=staffID, studentID=studentID, requestText=requestText)
    return newrequest

def send_request(staffID, studentID, requestText):
    staff = get_staff(staffID)
    stud = get_student(studentID)
    
    if(staff):
        if(stud):
            newrequest = create_request(staffID, studentID, requestText)
            try:
                db.session.add(newrequest)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return None

            send_notification(staffID,studentID,requestText)
    
def get_request(reuestID):
    return request.query.get(requestID)

def get_all_requests():
    return Request.query.all()

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

def approve_request(requestID, notifID, status):
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