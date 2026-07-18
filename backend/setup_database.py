import os
import sys
from datetime import date

# Add the backend directory to python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import create_app
from src.models import db, User, Task

app = create_app()


def setup():
    with app.app_context():
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
            tasks = [
                Task(
                    title="Städa badrum",
                    user_id=marcus.id,
                    due_date=date.today(),
                    emoji="🧽",
                    details="Glöm inte att torka av spegeln.",
                    is_recurring=True,
                    interval_type="weeks",
                    interval_value=1,
                    specific_day=3,  # Thursday
                ),
                Task(
                    title="Rengör ugn",
                    user_id=vida.id,
                    due_date=date.today(),
                    emoji="🔥",
                    details=None,
                    is_recurring=True,
                    interval_type="months",
                    interval_value=3,
                    specific_day=1,
                ),
                Task(
                    title="Sortera viktiga papper",
                    user_id=marcus.id,
                    due_date=date.today(),
                    emoji="📄",
                    details=None,
                    is_recurring=True,
                    interval_type="years",
                    interval_value=1,
                    specific_day=None,
                ),
            ]
            db.session.add_all(tasks)
            db.session.commit()

        print("Database setup complete!")


if __name__ == "__main__":
    setup()
