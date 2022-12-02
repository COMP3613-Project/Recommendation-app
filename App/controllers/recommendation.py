from App.models import Recommendation, Student
from App.database import db
from sqlalchemy.exc import IntegrityError

def create_recommendation(staffID, studentID, recomText):
    newrec = Recommendation(staffID=staffID, studentID=studentID, recomText=recomText)
    return newrec

def send_recommendation(sentFromStaffID, sentToStudentID, recURL):
    student = Student.query.get(sentToStudentID)
    newrec = create_recommendation(sentFromStaffID, sentToStudentID, recURL)
    try:
        db.session.add(newrec)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None
    student.recommendationList.append(newrec)
    try:
        db.session.add(student)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None
    return student

def get_all_recommendations():
    return Recommendation.query.all()

def get_all_recommendations_json():
    recs = get_all_recommendations()
    if not recs:
        return None
    recs = [rec.toJSON() for rec in recs]
    return recs

def get_recommendation(studentID, recID):
    rec = Recommendation.query.filter_by(sentToStudentID=studentID, recID=recID).first()
    if rec:
        return rec.toJSON()
    return None



