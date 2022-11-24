from App.database import db

Class Request(model)

	requestID= db.Column(db.Integer, primaryKey= True)
	studentID= db.Column(db.Integer, db.ForeignKey('student.studentID'), primary_key = True)
staffID= db.Column(db.String, db.ForeignKey('staff.staffId'),primary_key= True)
	title= db.Column(db.String, nullable= False)
	requestText= db.Column(db.String, nullable= False)
      date= db.Column(db.String, nullable =False)
	request= db.relationship('Request', backref= db.backref('Request', lazy='joined')


def_init_(self,studentID, staffID,title,requestText,date):
		self.studentID=studentID
		self.staffID=staffID
		self.title=title
		self.requestText=requestText
		self.date=date

def toJSON(self)
    return{
		'requestID':self.requestID,
		'studentID':self.studentID,
  		'staffID': self.staffID,
 		'title':self.title,
		'requestText':self.requestText,
		'date': self.date,
		'request': [req.toJson() for Request in self.request]
}

def toJSON_Request(self)
    return{
		'requestID':self.requestID,
		'studentID':self.studentID,
  		'staffID': self.staffID,
 		'title':self.title,
		'requestText':self.requestText,
		'date': self.date,
		request:[req.toJSON() for Request in self.request]

