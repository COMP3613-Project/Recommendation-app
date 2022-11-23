from App.database import db
class Recommendation(db.Model):
    recomID = db.Column(db.Integer, primary_key=True)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID'))
    staffName= db.Column(db.String, db.'staff.staffName'))
    recomText= db.Column(db.String, nullable=False)
    date= db.Column(db.String,nuallable=False)
    recomList= db.relationship('recomList',backref=db.backref(Recommendation, lazy='joined'))

    def __init__(self,staffID, studentID,staffName, recomText,date ):
        self.staffID=staffID
        self.studentID= studentID
        self.staffName=staffName
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
def toJSON_Recom(self):
        return{
            'recomID'  : self.recomID,
            'staffID'  : self.staffID,
            'studentID': self.studentID,
            'staffName': self.staffName,
            'recomText': self.recomText,
            'date'     : self.date,
            'recomList': [recom.toJSON() for recom in self.recomList]
            
        }

    
    
