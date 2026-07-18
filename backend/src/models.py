from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# pylint: disable=too-few-public-methods


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)

    def to_dict(self) -> dict:
        return {"id": self.id, "username": self.username}


class Task(db.Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)

    status: Mapped[str] = mapped_column(default="pending")  # 'pending' or 'done'
    due_date: Mapped[date] = mapped_column(nullable=False)

    details: Mapped[str | None] = mapped_column()
    emoji: Mapped[str | None] = mapped_column(default="📝")

    is_recurring: Mapped[bool] = mapped_column(default=False)
    interval_type: Mapped[str | None] = (
        mapped_column()
    )  # 'days', 'weeks', 'months', 'years'
    interval_value: Mapped[int | None] = mapped_column()
    specific_day: Mapped[int | None] = mapped_column()  # 0-6 for weeks, 1-31 for months

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "user_id": self.user_id,
            "status": self.status,
            "due_date": self.due_date.isoformat(),
            "details": self.details,
            "emoji": self.emoji,
            "is_recurring": self.is_recurring,
            "interval_type": self.interval_type,
            "interval_value": self.interval_value,
            "specific_day": self.specific_day,
            "created_at": self.created_at.isoformat(),
        }
