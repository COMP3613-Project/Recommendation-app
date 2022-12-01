import os, tempfile, pytest, logging, unittest, datetime
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db
from App.models import *
from App.controllers import (
    create_user,
    authenticate,
    get_all_users_json,
    get_all_staff_json,
    get_all_students_json,
    search_staff,
    create_notification,
    change_status,
    get_all_notifs_json,
    create_recommendation,
    get_all_recommendations_json
)

from wsgi import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    # test_new_student()
    def test_new_student(self):
        newstudent = Student("rob@mail.com", "Rob", "Singh", "student", "pass")
        assert newstudent.firstName == "Rob", newstudent.lastName == "Singh"
        assert newstudent.email == "rob@mail.com", newstudent.userType=="student"

    # test_new_staff()
    def test_new_staff(self):
        newstaff = Staff("bob@mail.com", "Bob", "Jones", "staff", "pass")
        assert newstaff.firstName == "Bob", newstaff.lastName == "Jones"
        assert newstaff.email == "bob@mail.com", newstaff.userType=="staff"

    # pure function no side effects or integrations called
    # test_student_toJSON()
    def test_student_toJSON(self):
        student = Student("rob@mail.com", "Rob", "Singh", "student", "pass")
        student_json = student.toJSON()
        self.assertDictEqual(student_json, {"studentID":None, "email":"rob@mail.com", "userType":"student", "firstName":"Rob","lastName":"Singh"})

    # test_staff_toJSON()
    def test_staff_toJSON(self):
        staff = Staff("bob@mail.com", "Bob", "Jones", "staff", "pass")
        staff_json = staff.toJSON()
        self.assertDictEqual(staff_json, {"staffID":None, "email":"bob@mail.com", "userType":"staff", "firstName":"Bob","lastName":"Jones"})

    # test_hashed_password()
    def test_hashed_password(self):
        password = "pass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("rob@mail.com", "Rob", "Singh", "student", password)
        assert user.password != password
    
    #test_check_password()
    def test_check_password(self):
        password = "pass"
        user = User("bob@mail.com", "Bob", "Jones", "staff", password)
        assert user.check_password(password) != password

    #test_new_recommendation()
    def test_new_recommendation(self):
        newrec = Recommendation("1", "1", "I hereby recommend you.")
        assert newrec.staffID=="1", newrec.studentID =="1"
        assert newrec.recomText =="I hereby recommend you."

    #test_rec_toJSON()
    def test_rec_toJSON(self):
        rec = Recommendation("1", "1", "I hereby recommend you.")
        current_time = datetime.now()
        test_time = current_time.strftime("%d/%m/%Y %H:%M")
        rec_json = rec.toJSON()
        self.assertDictEqual(rec_json, {"recomID":None, "staffID":"1", "studentID":"1", "recomText":"I hereby recommend you.", "date":test_time}) 
    
    #test_new_request()
    def test_new_request(self):
        newrequest = Request("1", "1", "Please send a recommendation to me")
        assert newrequest.studentID == "1", newrequest.staffID == "1" 
        assert newrequest.requestText== "Please send a recommendation to me"

    #test_request_toJSON()
    def test_request_toJSON(self):
        newrequest = Request("1", "1", "Please send a recommendation to me")
        current_time = datetime.now()
        test_time = current_time.strftime("%d/%m/%Y %H:%M")
        newrequest_json = newrequest.toJSON()
        self.assertDictEqual(newrequest_json,{"requestID":None, "staffID": "1", "studentID":"1", "requestText":"Please send a recommendation to me", "date":test_time, "status":"pending"})

    #test_new_notification()
    def test_new_notification(self):
        newnotif = Notification("1", "1", "Please send a recommendation to me")
        assert newnotif.requestID=="1", newnotif.staffID =="1"
        assert newnotif.requestTitle =="Please send a recommendation to me", newnotif.status =="unread"

    #test_notif_toJSON()
    def test_notif_toJSON(self):
        notif = Notification("1", "1", "Please send a recommendation to me")
        current_time = datetime.now()
        test_time = current_time.strftime("%d/%m/%Y %H:%M")
        notif_json = notif.toJSON()
        self.assertDictEqual(notif_json, {"notifID":None, "requestID": "1", "staffID":"1", "requestTitle":"Please send a recommendation to me", "date":test_time})