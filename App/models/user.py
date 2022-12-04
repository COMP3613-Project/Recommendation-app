from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email =  db.Column(db.String, unique=True,nullable=False)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    userType = db.Column(db.String, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    student = db.relationship('Student',backref=db.backref('user',lazy='joined'))
    staff = db.relationship('Staff',backref=db.backref('user',lazy='joined'))

    def __init__(self, email, firstName, lastName,userType, password):
        self.email = email
        self.firstName=firstName
        self.lastName=lastName
        self.userType=userType
        self.set_password(password)

    def toJSON(self):
        return{
            'id'       : self.id,
            'email'    : self.email,
            'firstName': self.firstName,
            'lastName' : self.lastName,
            'userType' : self.userType
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

#written by KARISHMA JAMES 