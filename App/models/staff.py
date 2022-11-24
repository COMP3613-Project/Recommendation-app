from App.database import db


class Staff(User):
    staffID = db.Column(db.Integer, db.ForeignKey('user.id'))
    # staff has a list of notification objects
    notificationFeed = db.relationship('Notification', backref=db.backref('staff', lazy='joined'))
    
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