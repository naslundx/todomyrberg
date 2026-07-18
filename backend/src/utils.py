from datetime import date, timedelta
from typing import Optional
import math


def calculate_snooze_days(interval_type: str, interval_value: int) -> int:
    base_days = 0
    if interval_type == "days":
        base_days = interval_value
    elif interval_type == "weeks":
        base_days = interval_value * 7
    elif interval_type == "months":
        base_days = interval_value * 30
    elif interval_type == "years":
        base_days = interval_value * 365
    else:
        return 1

    snooze = math.ceil(base_days * 0.1)
    return max(1, snooze)


def calculate_next_due_date(
    from_date: date,
    interval_type: str,
    interval_value: int,
    specific_day: Optional[int],
    force_at_least_7_days: bool = False,
) -> date:
    next_date = from_date

    if interval_type == "days":
        next_date += timedelta(days=interval_value)
    elif interval_type == "weeks":
        next_date += timedelta(weeks=interval_value)
        if specific_day is not None:
            # specific_day: 0 = Monday, 6 = Sunday
            current_weekday = next_date.weekday()
            days_ahead = specific_day - current_weekday
            if days_ahead < 0:
                days_ahead += 7
            next_date += timedelta(days=days_ahead)

            # If we need to ensure it's at least 7 days from now (from_date)
            # because of 'tidigt klar' rule
            if force_at_least_7_days:
                while (next_date - from_date).days < 7:
                    next_date += timedelta(weeks=1)

    elif interval_type == "months":
        # approximate month addition, then set specific day if provided
        months_to_add = interval_value
        new_month = next_date.month - 1 + months_to_add
        new_year = next_date.year + new_month // 12
        new_month = new_month % 12 + 1

        target_day = specific_day if specific_day is not None else next_date.day
        # Handle month length
        while True:
            try:
                next_date = date(new_year, new_month, target_day)
                break
            except ValueError:
                target_day -= 1  # back up to end of month
    elif interval_type == "years":
        new_year = next_date.year + interval_value
        try:
            next_date = date(new_year, next_date.month, next_date.day)
        except ValueError:
            # Leap year handling (Feb 29)
            next_date = date(new_year, next_date.month, 28)

    return next_date
