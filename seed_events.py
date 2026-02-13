from app import create_app
from database import db
from models import Group, Event
from datetime import datetime, timedelta
import random

app = create_app()

with app.app_context():

    group = Group.query.filter_by(name="Team Alpha").first()

    if not group:
        print("Team Alpha not found!")
        exit()

    print("Adding events to Team Alpha...")

    base_dates = [
        datetime(2026, 2, 3, 9),
        datetime(2026, 2, 6, 13),
        datetime(2026, 2, 10, 10),
        datetime(2026, 2, 14, 8),
        datetime(2026, 2, 18, 14),
        datetime(2026, 2, 22, 11),
        datetime(2026, 2, 26, 9),
        datetime(2026, 3, 2, 10),
        datetime(2026, 3, 7, 13),
        datetime(2026, 3, 12, 15),
        datetime(2026, 3, 18, 9),
        datetime(2026, 3, 25, 11),
    ]

    titles = [
        "Sprint Planning",
        "Team Meeting",
        "Client Demo",
        "Deployment",
        "Design Workshop",
        "Code Review",
        "Architecture Session",
        "Product Review",
        "Backend Refactor",
        "Security Audit",
        "Roadmap Discussion",
        "Performance Testing",
    ]

    for i in range(len(base_dates)):
        start_time = base_dates[i]
        duration_hours = random.choice([1, 2, 3])
        end_time = start_time + timedelta(hours=duration_hours)

        event = Event(
            title=titles[i],
            start_time=start_time,
            end_time=end_time,
            group_id=group.id
        )

        db.session.add(event)

    db.session.commit()

    print("12 events created successfully.")
