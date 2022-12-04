from App.database import db
from App.models import User


class Student(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, autoincrement=True)
    # student has a list of recommendation objects
    requests = db.relationship('Request',backref=db.backref('student',lazy='joined'))
    recomlist = db.relationship('Recommendation', backref=db.backref('student', lazy='joined'))

    def __init__(self, email, firstName, lastName,userType, password):
        super(Student, self).__init__(email, firstName, lastName,userType, password)
    
    def toJSON(self):
        return{
            'id': self.id,
            'email'    : self.email,
            'firstName': self.firstName,
            'lastName' : self.lastName,
            'userType' : self.userType
        }
        
    def toJSON_Recoms(self):
        return{
            
            'id' : self.id,
            'email'     : self.email,
            'firstName' : self.firstName,
            'lastName'  : self.lastName,
            'userType'  : self.userType,
            'recommendationList': [recommendation.toJSON() for recommendation in self.recomList]
        }
        #written by KARISHMA JAMES