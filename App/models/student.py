from App.database import db
from App.models import User

class Student(User):
    studentID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    # student has a list of recommendation objects
    recomList = db.relationship('Recommendation', backref=db.backref('student', lazy='joined'))
    
    def toJSON(self):
        return{
            'studentID': self.studentID,
            'email': self.email,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'userType': self.userType,
        }
        
    def toJSON_Recoms(self):
        return{
            
            'studentID': self.studentID,
            'email': self.email,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'userType': self.userType
            'recommendationList': [recommendation.toJSON() for recommendation in self.recomList]
        }