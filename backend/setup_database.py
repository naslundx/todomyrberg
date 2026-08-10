import csv
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

            print("Adding example tasks from CSV...")
            existing_task_titles = {t.title for t in Task.query.all()}
            
            today = date.today()
            
            # We need a dictionary to map usernames to User objects easily
            users_map = {u.username: u for u in User.query.all()}
            
            tasks = []
            csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "initial_tasks.csv")
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['title'] in existing_task_titles:
                        continue
                    
                    # Parse users
                    usernames = row['users'].split(';')
                    task_users = [users_map[u_name.strip()] for u_name in usernames if u_name.strip() in users_map]
                    
                    # Parse random offset
                    offset_days = int(row['random_offset_days']) if row['random_offset_days'] else 0
                    
                    # Parse specific day
                    specific_day = int(row['specific_day']) if row.get('specific_day') else None
                    
                    tasks.append(
                        Task(
                            title=row['title'],
                            users=task_users,
                            due_date=today + random_offset(offset_days),
                            emoji=row['emoji'],
                            is_recurring=row['is_recurring'].lower() == 'true',
                            interval_type=row['interval_type'],
                            interval_value=int(row['interval_value']) if row['interval_value'] else None,
                            specific_day=specific_day,
                        )
                    )
                    
            if tasks:
                db.session.add_all(tasks)
                db.session.commit()
                print(f"Added {len(tasks)} new tasks.")
            else:
                print("No new tasks to add.")

            print("Database setup complete!")

        except IntegrityError:
            db.session.rollback()
            print("Database setup encountered an integrity error.")
        except Exception as e:  # pylint: disable=broad-exception-caught
            db.session.rollback()
            print(f"Database setup failed: {e}")
