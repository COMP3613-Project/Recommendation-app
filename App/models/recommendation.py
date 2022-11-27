from App.database import db

class Recommendation(db.Model):
    recomID = db.Column(db.Integer, primary_key=True)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID'))
    recomText= db.Column(db.String, nullable=False)
    date= db.Column(db.String,nuallable=False)
    

    def __init__(self,staffID, studentID, recomText,date ):
        self.staffID=staffID
        self.studentID= studentID
        self.recomText= recomText
        self.date=date
    
    def toJSON(self):
        return{
            'recomID'  : self.recomID,
            'staffID'  : self.staffID,
            'studentID': self.studentID,
            'staffName': self.staffName,
            'recomText': self.recomText,
            'date'     : self.date
            
        }

    #written by KARISHMA JAMES
    
