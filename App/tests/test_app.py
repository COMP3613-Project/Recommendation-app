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
    get_all_requests_json,
    search_staff,
    create_notification,
    change_status,
    get_all_notifs_json,
    create_recommendation,
    get_all_recommendations_json,
    create_request,
    get_all_requests
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


'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')

# test_authenticate()
def test_authenticate():
    user = create_user("bob@mail.com", "Bob", "Jones", "staff", "pass")
    try:
        db.session.add(user)
    except:
        db.session.rollback()
    assert authenticate(user.email,"pass") != None
    db.session.remove()

class UsersIntegrationTests(unittest.TestCase):

    # test_create_user()
    def test_create_user(self):
        user = create_user("rob@mail.com", "Rob", "Singh", "student", "pass")
        assert user.email == "rob@mail.com", user.firstName == "Rob"

    # test_get_all_users_json()
    def test_get_all_users_json(self):
        user1 = create_user("bob@mail.com", "Bob", "Jones", "staff", "pass")
        db.session.add(user1)
        user2 = create_user("rob@mail.com", "Rob", "Singh", "student", "pass")   
        db.session.add(user2)
        
        users_json = get_all_users_json()
        
        db.session.remove()
        
        self.assertListEqual([{"id":1, "email":"bob@mail.com", "firstName":"Bob", "lastName":"Jones", "userType":"staff"},
                              {"id":2, "email":"rob@mail.com", "firstName":"Rob", "lastName":"Singh", "userType":"student"}],
                             users_json)

    # test_get_all_students_json()
    def test_get_all_students_json(self):
        user1 = create_user("bob@mail.com", "Bob", "Jones", "staff", "pass")
        user2 = create_user("rob@mail.com", "Rob", "Singh", "student", "pass")
        user3 = create_user("chloe@mail.com", "Chloe", "Smith", "student", "mypass")
        
        try:
            db.session.add(user1)
            db.session.add(user2)
            db.session.add(user3)
        except:
            db.session.rollback()
            
        students_json = get_all_students_json()
        
        self.assertListEqual([{"studentID":2, "email":"rob@mail.com",  "firstName":"Rob", "lastName":"Singh", "userType":"student"},
                              {"studentID":3, "email":"chloe@mail.com", "firstName":"Chloe", "lastName":"Smith","userType":"student"}],
                             students_json)
        db.session.remove()

    # test_get_all_staff_json()
    def test_get_all_staff_json(self):
        user1 = create_user("bob@mail.com", "Bob", "Jones", "staff", "pass")
        user2 = create_user("rob@mail.com", "Rob", "Singh", "student", "pass")
        user3 = create_user("j@mail.com", "John", "Smith", "staff", "mypass")
        
        try:
            db.session.add(user1)
            db.session.add(user2)
            db.session.add(user3)
        except:
            db.session.rollback()
            
        staff_json = get_all_staff_json()
        
        self.assertListEqual([{"staffID":1, "email":"bob@mail.com", "firstName":"Bob", "lastName":"Jones", "userType":"staff"},
                              {"staffID":3, "email":"j@mail.com", "firstName":"John", "lastName":"Smith", "userType":"staff"}],
                             staff_json)
        db.session.remove()

    # test_search_staff
    def test_search_staff(self):
        user1 = create_user("bob@mail.com", "Bob", "Jones", "staff", "pass")
        user2 = create_user("rob@mail.com", "Rob", "Singh", "student", "pass")
        user3 = create_user("j@mail.com", "John", "Smith", "staff", "mypass")
        
        try:
            db.session.add(user1)
            db.session.add(user2)
            db.session.add(user3)
        except:
            db.session.rollback()
            
        staff = search_staff("ID", "1")
        
        db.session.remove()
        
        self.assertDictEqual({"staffID":1, "email":"bob@mail.com", "firstName":"Bob", "lastName":"Jones", "userType":"staff"},
                             staff)
    
    # test_create_request
    def test_create_request(self):
        staff = create_user("bob@mail.com", "Bob", "Jones", "staff", "pass")
        student = create_user("rob@mail.com", "Rob", "Singh", "student", "pass")

        request = create_request(staff.staffID,student.studentID,"I need a recommendation")

        assert request.staffID == staff.staffID

    # test_get_request
    def test_get_request(self):
        staff = create_user("bob@mail.com", "Bob", "Jones", "staff", "pass")
        student = create_user("rob@mail.com", "Rob", "Singh", "student", "pass")

        try:
            db.session.add(staff)
            db.session.add(student)
        except:
            db.session.rollback
        
        request = create_request(staff.staffID,student.studentID,"I need a recommendation")
        current_time = datetime.now()
        test_time = current_time.strftime("%d/%m/%Y %H:%M")
       
        db.session.add(request)
        
        request = Request.query.get(1)
        db.session.remove()
        self.assertDictEqual({"requestID":1, "staffID": None, "studentID":None, "requestText":"I need a recommendation", "date":test_time, "status":"pending"},
                             request.toJSON())
    
    # test_get_all_requests_json()
    def test_get_all_requests_json(self):
        
        staff = create_user("bob@mail.com", "Bob", "Jones", "staff", "pass")
        student = create_user("rob@mail.com", "Rob", "Singh", "student", "pass")
        
        try:
            db.session.add(staff)
            db.session.add(student)
        except:
            db.session.rollback
        
        request = create_request(staff.staffID,student.studentID,"I need a recommendation")
        current_time = datetime.now()
        test_time = current_time.strftime("%d/%m/%Y %H:%M")
        db.session.add(request)
        
        request = create_request(staff.staffID,student.studentID,"Please write me a recommendation")
        current_time = datetime.now()
        test_time = current_time.strftime("%d/%m/%Y %H:%M")
        db.session.add(request)
        
        requests_json = get_all_requests_json()
        
        db.session.remove()
        
        self.assertListEqual([{"requestID":1, "staffID": None, "studentID":None, "requestText":"I need a recommendation", "date":test_time, "status":"pending"},
                              {"requestID":2, "staffID": None, "studentID":None, "requestText":"Please write me a recommendation", "date":test_time, "status":"pending"}],
                             requests_json)


    # test_send_request
    def test_send_notification(self):
        staff = create_user("bob@mail.com", "Bob", "Jones", "staff", "pass")
        student = create_user("rob@mail.com", "Rob", "Singh", "student", "pass")
        
        try:
            db.session.add(staff)
            db.session.add(student)
        except:
            db.session.rollback
        
        request = create_request(staff.staffID,student.studentID,"I need a recommendation")
        notif = create_notification(request.requestID, student.studentID, "I need a recommendation")
        
        staff.notificationFeed.append(notif)
        db.session.remove()
                
        assert staff.notificationFeed != None

    # test_get_notification()
    def test_get_notification(self):
        staff = create_user("bob@mail.com", "Bob", "Jones", "staff", "pass")
        student = create_user("rob@mail.com", "Rob", "Singh", "student", "pass")
        
        try:
            db.session.add(staff)
            db.session.add(student)
        except:
            db.session.rollback
        
        request = create_request(staff.staffID,student.studentID,"I need a recommendation")
        notif = create_notification(request.requestID, student.studentID, request.requestText)
        current_time = datetime.now()
        test_time = current_time.strftime("%d/%m/%Y %H:%M")
        
        db.session.add(notif)
        
        notif = Notification.query.get(1)
        db.session.remove()
        self.assertDictEqual({"notifID":1, "requestID": request.requestID, "staffID":None, "requestTitle":"I need a recommendation", "date":test_time},
                             notif.toJSON())

    # test_get_all_notifications_json()
    def test_get_all_notifications_json(self):
        
        staff = create_user("bob@mail.com", "Bob", "Jones", "staff", "pass")
        student = create_user("rob@mail.com", "Rob", "Singh", "student", "pass")
        
        try:
            db.session.add(staff)
            db.session.add(student)
        except:
            db.session.rollback
        
        request = create_request(staff.staffID,student.studentID,"I need a recommendation")
        notif = create_notification(request.requestID, student.studentID, request.requestText)
        current_time = datetime.now()
        test_time = current_time.strftime("%d/%m/%Y %H:%M")
        db.session.add(notif)
        staff.notificationFeed.append(notif)
        
        request = create_request(staff.staffID,student.studentID,"Please write me a recommendation")
        notif = create_notification(request.requestID, student.studentID, request.requestText)
        current_time = datetime.now()
        test_time = current_time.strftime("%d/%m/%Y %H:%M")
        db.session.add(notif)
        staff.notificationFeed.append(notif)
        
        notifs_json = get_all_notifs_json()
        
        db.session.remove()
        
        self.assertListEqual([{"notifID":1, "requestID": None, "staffID":staff.staffID, "requestTitle":"I need a recommendation","date":test_time},
                              {"notifID":2, "requestID": None, "staffID":staff.staffID, "requestTitle":"Please write me a recommendation","date":test_time}],
                             notifs_json)

    # test_approve_request
    def test_approve_request(self):
        staff = create_user("bob@mail.com", "Bob", "Jones", "staff", "pass")
        student = create_user("rob@mail.com", "Rob", "Singh", "student", "pass")
        
        try:
            db.session.add(staff)
            db.session.add(student)
        except:
            db.session.rollback
        
        request = create_request(staff.staffID,student.studentID,"I need a recommendation")
        current_time = datetime.now()
        test_time = current_time.strftime("%d/%m/%Y %H:%M")
        notif = create_notification(request.requestID, student.studentID, request.requestText)
        db.session.add(notif)
        staff.notificationFeed.append(notif)
        
        change_status(request, "approved")
        
        db.session.remove()
        
        self.assertDictEqual({"requestID":None, "staffID": None, "studentID":None, "requestText":"I need a recommendation", "date":test_time, "status":"approved"},
                                request.toJSON())

    # test_send_recommendation
    def test_send_recommendation(self):
        staff = create_user("bob@mail.com", "Bob", "Jones", "staff", "pass")
        student = create_user("rob@mail.com", "Rob", "Singh", "student", "pass")
        
        try:
            db.session.add(staff)
            db.session.add(student)
        except:
            db.session.rollback
    
        newrec = create_recommendation(staff.staffID, student.studentID, "I hereby recommend you!")
        student.recomlist.append(newrec)
        
        db.session.remove()
        
        assert student.recomlist != None

    # test_get_recommendation()
    def test_get_notification(self):
        staff = create_user("bob@mail.com", "Bob", "Jones", "staff", "pass")
        student = create_user("rob@mail.com", "Rob", "Singh", "student", "pass")
        
        try:
            db.session.add(staff)
            db.session.add(student)
        except:
            db.session.rollback
        
        newrec = create_recommendation(staff.staffID, student.studentID, "I hereby recommend you!")
        current_time = datetime.now()
        test_time = current_time.strftime("%d/%m/%Y %H:%M")
        student.recomlist.append(newrec)
        db.session.add(newrec)
        
        newrec = Recommendation.query.get(1)
        db.session.remove()
        self.assertDictEqual({"recomID":1, "staffID":None, "studentID":student.studentID, "recomText":"I hereby recommend you!", "date":test_time},
                             newrec.toJSON())
    
    # test_get_all_recommendations_json()
    def test_get_all_recommendations_json(self):
        staff = create_user("bob@mail.com", "Bob", "Jones", "staff", "pass")
        student = create_user("rob@mail.com", "Rob", "Singh", "student", "pass")
        
        try:
            db.session.add(staff)
            db.session.add(student)
        except:
            db.session.rollback
        
        newrec = create_recommendation(staff.staffID, student.studentID, "I hereby recommend you!")
        current_time = datetime.now()
        test_time = current_time.strftime("%d/%m/%Y %H:%M")
        student.recomlist.append(newrec)
        db.session.add(newrec)
        
        newrec = create_recommendation(staff.staffID, student.studentID, "I hereby recommend you also!")
        student.recomlist.append(newrec)
        db.session.add(newrec)
        
        recs_json = get_all_recommendations_json()
        
        db.session.remove()
        
        self.assertListEqual([{"recomID":1, "staffID":None, "studentID":student.studentID, "recomText":"I hereby recommend you!", "date":test_time},
                              {"recomID":2, "staffID":None, "studentID":student.studentID, "recomText":"I hereby recommend you also!", "date":test_time}],
                             recs_json)
        
        
        