from app import create_app
from database import db
from models import User, Group, UserGroup

app = create_app()

with app.app_context():

    # ----- Create Groups -----
    group1 = Group(name="Team Alpha")
    group2 = Group(name="Team Beta")

    db.session.add_all([group1, group2])
    db.session.commit()

    # ----- Create Users -----
    admin = User(username="hans", is_admin=True)
    admin.set_password("admin123")

    user1 = User(username="user1")
    user1.set_password("password123")

    user2 = User(username="user2")
    user2.set_password("password123")

    db.session.add_all([admin, user1, user2])
    db.session.commit()

    # ----- Assign Users To Groups -----
    db.session.add(UserGroup(user_id=admin.id, group_id=group1.id, role="admin"))
    db.session.add(UserGroup(user_id=user1.id, group_id=group1.id, role="member"))
    db.session.add(UserGroup(user_id=user2.id, group_id=group2.id, role="member"))

    db.session.commit()

    print("Seed users and groups created successfully.")