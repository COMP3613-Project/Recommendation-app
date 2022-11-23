from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    email =  db.Column(db.String, unique=True,nullable=False)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    userType = db.Column(db.String, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, email, firstName, lastName,userType, password):
        self.email = email
        self.firstName=firstName
        self.lastName=lastName
        self.userType=userType
        self.set_password(password)

    def toJSON(self):
        return{
            'id': self.id,
            'email': self.email,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'userType': self.userType
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

