from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import text
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from app import db

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(4096),nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(255), nullable=True)
    lastname = db.Column(db.String(255), nullable=True)
    about = db.Column(db.String(4096),nullable=True)
    photo = db.Column(db.String(20), default='default.jpg')
    isAdmin = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.firstname}', '{self.lastname}', '{self.password}')"

class Classes(db.Model):
    __tablename__ = "classes"
    classID = db.Column(db.Integer, primary_key=True)
    classCode = db.Column(db.String(6),nullable=False)
    classAdminID = db.Column(db.Integer, db.ForeignKey("users.id"))
    classes_admin = db.relationship('Users', lazy=True, foreign_keys=[classAdminID])

    def __repr__(self):
        return f"User('{self.classID}', '{self.classCode}', '{self.classAdminID}')"

class ClassesUsers(db.Model):
    __tablename__="classusers"
    cuid = db.Column(db.Integer, primary_key=True)
    classID = db.Column(db.Integer, db.ForeignKey("classes.classID"))
    usersID = db.Column(db.Integer, db.ForeignKey("users.id"))
    class_r = db.relationship('Classes', lazy=True, foreign_keys=[classID])
    user_r = db.relationship('Users', lazy=True, foreign_keys=[usersID])


class Events(db.Model):
    __tablename__ = "events"
    eventID = db.Column(db.Integer, primary_key=True, nullable=False)
    eventType = db.Column(db.String(100), nullable=False)
    eventDistance = db.Column(db.Integer, nullable=True)
    eventTime = db.Column(db.Time, nullable=True)

class Logs(db.Model):
    __tablename__ = "logs"
    userID = db.Column(db.Integer, db.ForeignKey("users.id"))
    logID = db.Column(db.Integer, primary_key=True, nullable=False)
    logContent = db.Column(db.String)
    logDateTime = db.Column(db.DateTime, nullable=False)
    log_user = db.relationship('Users', lazy=True, foreign_keys=[userID])


class Photos(db.Model):
    __tablename__ = "postphotos"
    userID = db.Column(db.Integer, db.ForeignKey("users.id"))
    postID = db.Column(db.Integer, db.ForeignKey("posts.postID"))
    postPhotoID = db.Column(db.Integer, primary_key=True, nullable=False)
    postPhoto = db.Column(db.String(20), default='default.jpg')
    postDateTime = db.Column(db.DateTime, nullable=False)
    photos_user = db.relationship('Users', lazy=True, foreign_keys=[userID])
    photo_post = db.relationship('Posts', lazy=True, foreign_keys=[postID])



class Posts(db.Model):
    __tablename__ = "posts"
    userID = db.Column(db.Integer, db.ForeignKey("users.id"))
    postID = db.Column(db.Integer, primary_key=True)
    postContent = db.Column(db.String(255))
    isPosted = db.Column(db.Integer)
    postDateTime = db.Column(db.DateTime, nullable=False)
    user_post = db.relationship('Users', lazy=True, foreign_keys=[userID])


class ScheduledAssignments(db.Model):
    __tablename__ = "scheduledassignments"
    assignmentID = db.Column(db.Integer, primary_key=True)
    eventID = db.Column(db.Integer, db.ForeignKey("events.eventID"))
    scheduledDateTime = db.Column(db.DateTime, nullable=False)
    returnDateTime = db.Column(db.DateTime, nullable=False)
    schass_event = db.relationship('Events', lazy=True, foreign_keys=[eventID])


class UserDST(db.Model):
    __tablename__ = "userdst"
    userID = db.Column(db.Integer, db.ForeignKey("users.id"))
    eventID = db.Column(db.Integer, db.ForeignKey("events.eventID"))
    userDSTID = db.Column(db.Integer, primary_key=True)
    dstDateTime = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    userDistance = db.Column(db.Integer, nullable=False)
    userTime = db.Column(db.Time, nullable=False)
    userSpeed = db.Column(db.Integer, nullable=False)
    isAssignment = db.Column(db.Integer, nullable=False)
    dst_user = db.relationship('Users', lazy=True, foreign_keys=[userID])
    dst_event = db.relationship('Events', lazy=True, foreign_keys=[eventID])