from App.database import db
from datetime import datetime

class Recommendation(db.Model):
    recomID = db.Column(db.Integer, primary_key=True)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID'))
    recomText= db.Column(db.String, nullable=False)
    date= db.Column(db.String, nullable=False)
    

    def __init__(self,staffID, studentID, recomText, date ):
        self.staffID=staffID
        self.studentID= studentID
        self.recomText= recomText
        self.set_date(date)
    
    def toJSON(self):
        return{
            'recomID'  : self.recomID,
            'staffID'  : self.staffID,
            'studentID': self.studentID,
            'staffName': self.staffName,
            'recomText': self.recomText,
            'date'     : self.date
            
        }
    def set_date(self, date):
	#set current date and time
	    date_time = datetime.date_time()
	    self.date = date_time.strftime("%d/%m/%Y %H:%M")
    #written by KARISHMA JAMES
    
