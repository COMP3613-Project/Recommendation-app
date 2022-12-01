from App.database import db
from datetime import datetime

class Notification(db.Model):
    notifID = db.Column(db.Integer, primary_key=True)
    requestID= db.Column(db.Integer,db.ForeignKey('request.requestID'))
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    requestTitle = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    
    
    def __init__(self, requestID, staffID, requestTitle):
        self.requestID=requestID
        self.staffID=staffID
        self.requestTitle=requestTitle
        self.set_date()
        
        
    def toJSON(self):
        return{
            'notifID'     : self.notifID,
            'requestID'   : self.requestID,
            'staffID'     : self.staffID,
            'requestTitle': self.requestTitle,
            'date'        : self.date
        
        }
    def set_date(self):
	#set current date and time
	    date_time = datetime.now()
	    self.date = date_time.strftime("%d/%m/%Y %H:%M")
        #written by KARISHMA JAMES