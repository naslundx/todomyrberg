import os
import random
import sys
from datetime import date, timedelta

from sqlalchemy.exc import IntegrityError

# Add the backend directory to python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models import Task, User, db


def random_offset(days: int) -> timedelta:
    """Returns a random timedelta between 0 and `days`."""
    return timedelta(days=random.randint(0, days))


if __name__ == "__main__":
    from main import create_app

    app = create_app()
    with app.app_context():
        try:
            print("Creating tables...")
            db.create_all()

            print("Creating initial users...")
            marcus = User.query.filter_by(username="Marcus").first()
            if not marcus:
                marcus = User(username="Marcus")
                db.session.add(marcus)

            vida = User.query.filter_by(username="Vida").first()
            if not vida:
                vida = User(username="Vida")
                db.session.add(vida)

            db.session.commit()

            print("Adding example tasks...")
            if Task.query.count() == 0:
                today = date.today()
                tasks = [
                    Task(
                        title="Städa lilla badrummet",
                        users=[marcus],
                        due_date=today + random_offset(7),
                        emoji="🚿",
                        is_recurring=True,
                        interval_type="weeks",
                        interval_value=1,
                    ),
                    Task(
                        title="Städa stora badrummet",
                        users=[marcus],
                        due_date=today + random_offset(7),
                        emoji="🛁",
                        is_recurring=True,
                        interval_type="weeks",
                        interval_value=1,
                    ),
                    Task(
                        title="Rengör ugnen",
                        users=[marcus],
                        due_date=today + random_offset(60),
                        emoji="🔥",
                        is_recurring=True,
                        interval_type="months",
                        interval_value=2,
                    ),
                    Task(
                        title="Rengör diskmaskin",
                        users=[marcus],
                        due_date=today + random_offset(30),
                        emoji="🍽️",
                        is_recurring=True,
                        interval_type="months",
                        interval_value=1,
                    ),
                    Task(
                        title="Rengör kaffemaskin",
                        users=[marcus],
                        due_date=today + random_offset(30),
                        emoji="☕",
                        is_recurring=True,
                        interval_type="months",
                        interval_value=1,
                    ),
                    Task(
                        title="Gå igenom viktiga papper",
                        users=[vida],
                        due_date=today + random_offset(180),
                        emoji="📁",
                        is_recurring=True,
                        interval_type="months",
                        interval_value=6,
                    ),
                    Task(
                        title="Sortera nyinkomna papper",
                        users=[vida],
                        due_date=today + random_offset(30),
                        emoji="📄",
                        is_recurring=True,
                        interval_type="months",
                        interval_value=1,
                    ),
                    Task(
                        title="Rensa i förrådet",
                        users=[vida, marcus],
                        due_date=today + random_offset(180),
                        emoji="📦",
                        is_recurring=True,
                        interval_type="months",
                        interval_value=6,
                    ),
                    Task(
                        title="Bokslut",
                        users=[vida, marcus],
                        due_date=today + random_offset(30),
                        emoji="💰",
                        is_recurring=True,
                        interval_type="months",
                        interval_value=1,
                        specific_day=24,
                    ),
                    Task(
                        title="Ta hand om cyklar",
                        users=[marcus],
                        due_date=today + random_offset(21),
                        emoji="🚲",
                        is_recurring=True,
                        interval_type="weeks",
                        interval_value=3,
                    ),
                    Task(
                        title="Dammtorka",
                        users=[marcus],
                        due_date=today + random_offset(7),
                        emoji="🧹",
                        is_recurring=True,
                        interval_type="weeks",
                        interval_value=1,
                    ),
                    Task(
                        title="Kontrollera backup",
                        users=[marcus],
                        due_date=today + random_offset(180),
                        emoji="💾",
                        is_recurring=True,
                        interval_type="months",
                        interval_value=6,
                    ),
                    Task(
                        title="Testa brandvarnare",
                        users=[marcus],
                        due_date=today + random_offset(180),
                        emoji="🚨",
                        is_recurring=True,
                        interval_type="months",
                        interval_value=6,
                    ),
                    Task(
                        title="Frosta av frys",
                        users=[vida],
                        due_date=today + random_offset(365),
                        emoji="❄️",
                        is_recurring=True,
                        interval_type="years",
                        interval_value=1,
                    ),
                ]
                db.session.add_all(tasks)
                db.session.commit()

            print("Database setup complete!")

        except IntegrityError:
            db.session.rollback()
            print("Database setup encountered an integrity error.")
        except Exception as e:  # pylint: disable=broad-exception-caught
            db.session.rollback()
            print(f"Database setup failed: {e}")
