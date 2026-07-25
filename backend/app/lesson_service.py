from datetime import datetime, timedelta, timezone

from fastapi import UploadFile
from sqlmodel import Session, select

from app.config import get_settings
from app.models import Lesson, Homework, LessonStats
from app.pdf_service import extract_pdf_text


def normalize_code(code: str) -> str:
    return code.strip().upper()


async def process_lesson(
    session: Session,
    code: str,
    pdf: UploadFile,
) -> Lesson:

    lesson_code = normalize_code(code)

    # Read PDF temporarily in memory
    pdf_bytes = await pdf.read()

    extracted_text = extract_pdf_text(pdf_bytes)

    settings = get_settings()

    expiry_days = settings.delete_after_days

    expires_at = datetime.now(timezone.utc) + timedelta(
        days=expiry_days
    )

    existing = session.exec(
        select(Lesson).where(
            Lesson.code == lesson_code
        )
    ).first()

    if existing:
        existing.lesson_summary = ""
        existing.expires_at = expires_at

        session.add(existing)
        session.commit()
        session.refresh(existing)

        return existing


    lesson = Lesson(
    code=lesson_code,
    lesson_text=extracted_text,
    lesson_summary="",
    expires_at=expires_at,
)

    session.add(lesson)
    session.commit()
    session.refresh(lesson)


    stats = LessonStats(
        lesson_code=lesson.code,
        accessed=0,
        submitted=0,
    )

    session.add(stats)
    session.commit()


    return lesson



def get_lesson_by_code(
    session: Session,
    code: str,
) -> Lesson | None:

    return session.exec(
        select(Lesson).where(
            Lesson.code == normalize_code(code)
        )
    ).first()



def delete_lesson(
    session: Session,
    code: str,
) -> bool:

    lesson = get_lesson_by_code(
        session,
        code,
    )

    if not lesson:
        return False


    homework = session.exec(
        select(Homework).where(
            Homework.lesson_code == lesson.code
        )
    ).first()

    if homework:
        session.delete(homework)


    stats = session.exec(
        select(LessonStats).where(
            LessonStats.lesson_code == lesson.code
        )
    ).first()

    if stats:
        session.delete(stats)


    session.delete(lesson)
    session.commit()

    return True