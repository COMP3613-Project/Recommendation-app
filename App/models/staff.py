from App.database import db
from App.models import User


class Staff(User):
    staffID = db.Column(db.Integer, db.ForeignKey('user.ID'), primary_key=True)
    # staff has a list of notification objects
    notificationFeed = db.relationship('Notification', backref=db.backref('staff', lazy='joined'))
    requestList= db.relationship('Request', backref= db.backref('Request', lazy='joined'))
    
    def toJSON(self):
        return {
            'staffID'  : self.staffID,
            'email'    : self.email,
            'firstName': self.firstName,
            'lastName' : self.lastName,
            'userType' : self.userType
        }
    
    def toJSON_notifs(self):
        return {
            'staffID'  : self.staffID,
            'email'    : self.email,
            'firstName': self.firstName,
            'lastName' : self.lastName,
            'userType' : self.userType,
            'notificationFeed': [notif.toJSON() for notif in self.notificationFeed]
        }
#written by KARISHMA JAMES