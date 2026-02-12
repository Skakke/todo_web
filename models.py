from database import db
from werkzeug.security import generate_password_hash, check_password_hash

# Association table for many-to-many relationship (sharing)
user_tasks = db.Table(
    'user_tasks',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # Tasks this user owns
    owned_tasks = db.relationship("Task", backref="owner", lazy=True)

    # Tasks shared with this user (many-to-many)
    shared_tasks = db.relationship(
        "Task",
        secondary=user_tasks,
        back_populates="shared_with_users"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    # Owner of the task
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Users the task is shared with
    shared_with_users = db.relationship(
        "User",
        secondary=user_tasks,
        back_populates="shared_tasks"
    )
