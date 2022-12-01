from App.database import db
from App.models import User


class Student(User):
    studentID = db.Column(db.Integer, db.ForeignKey('user.ID'), primary_key=True)
    # student has a list of recommendation objects
    requests = db.relationship('Request',backref=db.backref('student',lazy='joined'))
    recomlist = db.relationship('Recommendation', backref=db.backref('student', lazy='joined'))
    
    def toJSON(self):
        return{
            'studentID': self.studentID,
            'email'    : self.email,
            'firstName': self.firstName,
            'lastName' : self.lastName,
            'userType' : self.userType
        }
        
    def toJSON_Recoms(self):
        return{
            
            'studentID' : self.studentID,
            'email'     : self.email,
            'firstName' : self.firstName,
            'lastName'  : self.lastName,
            'userType'  : self.userType,
            'recommendationList': [recommendation.toJSON() for recommendation in self.recomList]
        }
        #written by KARISHMA JAMES