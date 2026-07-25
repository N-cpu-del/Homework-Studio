from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Lesson(SQLModel, table=True):

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    code: str = Field(
        index=True,
        unique=True,
        max_length=64
    )

    lesson_text: str = ""

    lesson_summary: str = ""

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    expires_at: datetime


class Homework(SQLModel, table=True):

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    lesson_code: str

    content: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class LessonStats(SQLModel, table=True):

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    lesson_code: str

    accessed: int = 0

    submitted: int = 0


class HomeworkSubmission(SQLModel, table=True):

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    lesson_code: str

    student_answers: str

    score: int = 0

    feedback: str = ""