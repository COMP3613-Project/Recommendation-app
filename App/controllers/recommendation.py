from App.models import Recommendation, Student
from App.database import db
from sqlalchemy.exc import IntegrityError

def create_recommendation(staffID, studentID, recomText):
    newrec = Recommendation(staffID=staffID, studentID=studentID, recomText=recomText)
    return newrec

def send_recommendation(staffID, studentID, recURL):
    student = Student.query.get(studentID)
    newrec = create_recommendation(staffID, studentID, recURL)
    try:
        db.session.add(newrec)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None
    student.recomlist.append(newrec)
    try:
        db.session.add(student)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None
    return student

def get_all_recommendations():
    return Recommendation.query.all()
    
def get_student_recommendations(studentID):
    return Recommendation.query.filter_by(studentID=studentID).all()

def get_all_recommendations_json():
    recs = get_all_recommendations()
    if not recs:
        return None
    recs = [rec.toJSON() for rec in recs]
    return recs

def get_recommendation(studentID, recID):
    rec = Recommendation.query.filter_by(studentID=studentID, recomID=recID).first()
    if rec:
        return rec.toJSON()
    return None



