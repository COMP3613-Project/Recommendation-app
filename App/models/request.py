from App.database import db
from datetime import datetime

#written by KARISHMA JAMES 
class Request(db.model):

	requestID= db.Column(db.Integer, primaryKey= True)
	studentID= db.Column(db.Integer, db.ForeignKey('student.studentID'))
	staffID= db.Column(db.String, db.ForeignKey('staff.staffId'))
	title= db.Column(db.String, nullable= False)
	requestText= db.Column(db.String, nullable= False)
	date= db.Column(db.String, nullable= False)
    
	notification=db.relationship('Notification', backref= db.backref(staff,lazy='joined'))
	
	def _init_(self,studentID, staffID,title,requestText,date):
		self.studentID=studentID
		self.staffID=staffID
		self.title=title
		self.requestText=requestText
		self.set_date(date)

	def toJSON(self):
    	return{
		'requestID':self.requestID,
		'studentID':self.studentID,
  		'staffID'  : self.staffID,
 		'title'    :self.title,
		'requestText':self.requestText,
		'date'     : self.date,
		'request'  : [req.toJson() for Request in self.request]
}


	def set_date(self, date):
	#set current date and time
		date_time = datetime.date_time()
		self.date = date_time.strftime("%d/%m/%Y %H:%M")

