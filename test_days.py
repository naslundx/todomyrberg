from datetime import date, timedelta
from backend.src.utils import calculate_next_due_date

from_date = date(2024, 1, 1) # Monday
triggered = False
for specific_day in range(7):
    for interval_value in range(1, 4):
        next_date = calculate_next_due_date(from_date, "weeks", interval_value, specific_day)
        if (next_date - from_date).days < 7:
            print(f"Less than 7! {specific_day=} {interval_value=}")
            triggered = True
if not triggered:
    print("Never < 7 days")
