from App.database import db
from App.models import User


class Staff(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, autoincrement=True)
    # staff has a list of notification objects

    recommendations = db.relationship('Recommendation',backref=db.backref('staff',lazy='joined'))
    notificationFeed = db.relationship('Notification', backref=db.backref('staff', lazy='joined'))
    requestList= db.relationship('Request', backref= db.backref('Request', lazy='joined'))
    
    def toJSON(self):
        return {
            'id'  : self.id,
            'email'    : self.email,
            'firstName': self.firstName,
            'lastName' : self.lastName,
            'userType' : self.userType
        }
    
    def toJSON_notifs(self):
        return {
            'id'  : self.id,
            'email'    : self.email,
            'firstName': self.firstName,
            'lastName' : self.lastName,
            'userType' : self.userType,
            'notificationFeed': [notif.toJSON() for notif in self.notificationFeed]
        }
#written by KARISHMA JAMES