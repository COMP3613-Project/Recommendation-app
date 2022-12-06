from App.models import Notification, Staff, User
from App.database import db
from sqlalchemy.exc import IntegrityError
from App.controllers import get_staff

def create_notification(requestID,staffID,requestBody):
    newNotif = Notification(requestID=requestID,staffID=staffID, requestTitle=requestBody)
    return newNotif

def send_notification(requestID, requestBody, sentToStaffID):
    # get staff feed - notif list
    staff = get_staff(sentToStaffID)

    # new notif
    newNotif = create_notification(requestID, sentToStaffID, requestBody)
    try:
        db.session.add(newNotif)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None
    # add notif to list
    staff.notificationFeed.append(newNotif)
    try:
        db.session.add(staff)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None
    return staff

def get_all_notifs():
    return Notification.query.all()

def get_all_notifs_json():
    notifs = get_all_notifs()
    if not notifs:
        return None
    notifs = [notif.toJSON() for notif in notifs]
    return notifs

def get_notif_by_request(requestID):
    return Notification.query.filter_by(requestID=requestID).first()

def delete_notification(notification):
    db.session.delete(notification) # delete the object
    db.session.commit()
    return notification.notifID

# gets a notification from a user's notif feed
def get_user_notif(staffID, notifID):
    return Notification.query.filter_by(staffID=staffID, notifID=notifID).first()


    