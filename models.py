from database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class UserGroup(db.Model):
    __tablename__ = "user_groups"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), primary_key=True)

    role = db.Column(db.String(20), nullable=False, default="member")
    # allowed: "admin", "member"

    user = db.relationship("User", back_populates="group_links")
    group = db.relationship("Group", back_populates="member_links")

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # Global system admin
    is_admin = db.Column(db.Boolean, default=False)

    group_links = db.relationship("UserGroup", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_group_admin(self, group_id):
        link = next((g for g in self.group_links if g.group_id == group_id), None)
        return link and link.role == "admin"


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    member_links = db.relationship("UserGroup", back_populates="group")
    events = db.relationship("Event", back_populates="group")


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    group = db.relationship("Group", back_populates="events")

    def validate(self):
        if not self.title.strip():
            raise ValueError("Title cannot be empty")
        if self.end_time <= self.start_time:
            raise ValueError("End must be after start")
