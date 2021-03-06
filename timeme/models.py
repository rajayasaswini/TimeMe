from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy.sql import text
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from timeme import db, login_man, app
from flask_login import UserMixin
import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Ser

#function to allow a user to login
@login_man.user_loader
def getuser(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(4096),nullable=False, unique=True)
    password = db.Column(db.String(4096), nullable=False)
    firstname = db.Column(db.String(255), nullable=True)
    lastname = db.Column(db.String(255), nullable=True)
    about = db.Column(db.String(4096),nullable=True)
    birthday = db.Column(db.Date, nullable = False)
    photo = db.Column(db.String(20), default='default.jpg')
    isAdmin = db.Column(db.Integer, nullable=False)
    #getting a token for a user to reset their password
    def get_token(self, expire_s = 1800):
        s = Ser(app.config['SECRET_KEY'], expire_s)
        return s.dumps({'users_id':self.id}).decode('utf-8')
    #verify token for resetting password
    @staticmethod
    def verify_token(token):
        s = Ser(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['users_id']
        except:
            return None
        return Users.query.get(user_id)
    #when anything is queried from the table, it appears in this form
    def __repr__(self):
        return '{} {}'.format(str(self.firstname), str(self.lastname))

class Classes(db.Model):
    __tablename__ = "classes"
    classID = db.Column(db.Integer, primary_key=True)
    className = db.Column(db.String, nullable=False)
    classCode = db.Column(db.String(6),nullable=False)
    classAdminID = db.Column(db.Integer, db.ForeignKey("users.id"))
    classes_admin = db.relationship('Users', lazy=True, foreign_keys=[classAdminID])

    def __repr__(self):
        return '{}'.format(str(self.className))

class ClassesUsers(db.Model):
    __tablename__="classusers"
    cuid = db.Column(db.Integer, primary_key=True)
    classID = db.Column(db.Integer, db.ForeignKey("classes.classID"))
    usersID = db.Column(db.Integer, db.ForeignKey("users.id"))
    class_r = db.relationship('Classes', lazy=True, foreign_keys=[classID])
    user_r = db.relationship('Users', lazy=True, foreign_keys=[usersID])

class EventTypes(db.Model):
    __tablename__="eventtypes"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '{}'.format(str(self.type))

class Events(db.Model):
    __tablename__ = "events"
    eventID = db.Column(db.Integer, primary_key=True, nullable=False)
    eventTypeID = db.Column(db.Integer,db.ForeignKey("eventtypes.id"), nullable=False)
    eventDistance = db.Column(db.Integer, nullable=True)
    eventTime = db.Column(db.Integer, nullable=True)
    eventT_r = db.relationship('EventTypes', lazy=True, foreign_keys=[eventTypeID])

class ScheduledAssignments(db.Model):
    __tablename__ = "scheduledassignments"
    assignmentID = db.Column(db.Integer, primary_key=True)
    classID = db.Column(db.Integer, db.ForeignKey("classes.classID"))
    eventID = db.Column(db.Integer, db.ForeignKey("events.eventID"))
    scheduledDate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    returnDate = db.Column(db.Date, nullable=False)
    schass_event = db.relationship('Events', lazy=True, foreign_keys=[eventID])
    schass_class = db.relationship('Classes', lazy=True, foreign_keys=[classID])

    def __repr__(self):
        date = self.returnDate
        eventID = self.eventID
        return "['{}-{}-{}']".format(str(date.year), str(date.month), str(date.day))

class ReturnedAssignment(db.Model):
    __tablename__ = "returnedassignments"
    rassid = db.Column(db.Integer, primary_key=True)
    schassid = db.Column(db.Integer, db.ForeignKey("scheduledassignments.assignmentID"))
    userdstid = db.Column(db.Integer, db.ForeignKey("userdst.userDSTID"))
    isLate = db.Column(db.Integer)
    rass_dst = db.relationship('UserDST', lazy=True, foreign_keys=[userdstid])
    rass_schass = db.relationship('ScheduledAssignments', lazy=True, foreign_keys=[schassid])

class UserDST(db.Model):
    __tablename__ = "userdst"
    userID = db.Column(db.Integer, db.ForeignKey("users.id"))
    eventID = db.Column(db.Integer, db.ForeignKey("events.eventID"))
    userDSTID = db.Column(db.Integer, primary_key=True)
    dstDateTime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    userDistance = db.Column(db.Integer, nullable=False)
    userTime = db.Column(db.Integer, nullable=False)
    userSpeed = db.Column(db.Integer, nullable=False)
    isAssignment = db.Column(db.Integer, nullable=False)
    dst_user = db.relationship('Users', lazy=True, foreign_keys=[userID])
    dst_event = db.relationship('Events', lazy=True, foreign_keys=[eventID])

class Registers(db.Model):
    __tablename__ = "registers"
    regid = db.Column(db.Integer, primary_key=True)
    classID = db.Column(db.Integer, db.ForeignKey("classes.classID"))
    date = db.Column(db.DateTime, nullable=False, default=date.today())
    class_reg = db.relationship('Classes', lazy=True, foreign_keys=[classID])

class RegPresent(db.Model):
    __tablename__ = "regpresent"
    regid = db.Column(db.Integer, db.ForeignKey("registers.regid"))
    registerid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("users.id"))
    user_reg = db.relationship('Users', lazy=True, foreign_keys=[userid])
    reg_reg = db.relationship('Registers', lazy=True, foreign_keys=[regid])

class Intervals(db.Model):
    __tablename__ = "interval"
    intervalid = db.Column(db.Integer, primary_key=True)
    userdstid = db.Column(db.Integer, db.ForeignKey("userdst.userDSTID"))
    dist = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    dst_interval = db.relationship('UserDST', lazy=True, foreign_keys=[userdstid])
