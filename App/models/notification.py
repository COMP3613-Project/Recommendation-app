from App.database import db

class Notification(db.Model):
    notifID = db.Column(db.Integer, primary_key=True)
    requestID= db.Column(db.Integer,db.ForeignKey('request.requestID'))
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    requestTitle = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    
    
def __init__(self, requestID staffID, requestTitle,date):
        self.requestID=requestID
        self.staffID=staffID
        self.requestTitle=requestTitle
        self.date=date
        
        
    def toJSON(self):
        return{
            'notifID'     : self.notifID,
            'requestID'   : self.requestID,
            'staffID'     : self.staffID,
            'requestTitle': self.requestTitle,
            'date'        : self.date
        
        }
    
        #written by KARISHMA JAMES