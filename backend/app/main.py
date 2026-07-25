import json

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session

from app.ai_service import AiService, AiServiceError
from app.config import get_settings
from app.database import create_db_and_tables, get_session
from app.lesson_service import (
    process_lesson,
    get_lesson_by_code,
    delete_lesson,
)
from app.pdf_service import PdfExtractionError
from app.models import Homework, HomeworkSubmission

from app.schemas import (
    GenerateHomeworkRequest,
    CreateLessonResponse,
    TeacherLoginRequest,
    TeacherLoginResponse,
)


settings = get_settings()


app = FastAPI(
    title="Homework Studio",
    version="2.0.0"
)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


@app.on_event("startup")
def startup():
    create_db_and_tables()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


ai_service = AiService()


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/api/teacher/login")
def teacher_login(
    request: TeacherLoginRequest
):

    return {
        "success":
        request.access_code == settings.teacher_access_code
    }


@app.post("/api/teacher/lessons")
async def upload_lesson(
    lesson_code: str = Form(...),
    pdf: UploadFile = File(...),
    session: Session = Depends(get_session)
):

    if pdf.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    try:
        lesson = await process_lesson(
            session,
            lesson_code,
            pdf
        )

    except PdfExtractionError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc)
        )

    return {
        "lesson_code": lesson.code,
        "message": "Lesson uploaded successfully."
    }


@app.post("/api/homework/generate")
def generate_homework(
    request: GenerateHomeworkRequest,
    session: Session = Depends(get_session)
):

    print("GENERATE ENDPOINT REACHED")

    lesson = get_lesson_by_code(
        session,
        request.lesson_code
    )

    if not lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found."
        )


    existing_homework = session.query(Homework).filter(
        Homework.lesson_code == lesson.code
    ).first()


    if existing_homework:

        homework_data = json.loads(
            existing_homework.content
        )

        if "lesson_code" not in homework_data:
            homework_data["lesson_code"] = lesson.code

        return homework_data



    try:

        print("CALLING AI GENERATE HOMEWORK")

        result = ai_service.generate_homework(
            lesson.code,
            lesson.lesson_text
        )


        result["lesson_code"] = lesson.code


        homework = Homework(
            lesson_code=lesson.code,
            content=json.dumps(result)
        )


        session.add(homework)
        session.commit()


    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"{type(exc).__name__}: {str(exc)}"
        )


    return result



@app.delete("/api/teacher/lessons/{lesson_code}")
def remove_lesson(
    lesson_code: str,
    session: Session = Depends(get_session)
):

    if not delete_lesson(
        session,
        lesson_code
    ):
        raise HTTPException(
            status_code=404,
            detail="Lesson not found."
        )


    return {
        "message": "Deleted"
    }



@app.get("/api/homework/{lesson_code}")
def get_homework(
    lesson_code: str,
    session: Session = Depends(get_session)
):

    homework = session.query(Homework).filter(
        Homework.lesson_code == lesson_code
    ).first()


    if not homework:
        raise HTTPException(
            status_code=404,
            detail="Homework not found."
        )


    return json.loads(
        homework.content
    )



@app.post("/api/homework/submit")
def submit_homework(
    lesson_code: str,
    answers: dict,
    session: Session = Depends(get_session)
):

    homework = session.query(Homework).filter(
        Homework.lesson_code == lesson_code
    ).first()


    if not homework:
        raise HTTPException(
            status_code=404,
            detail="Homework not found."
        )


    homework_json = json.loads(
        homework.content
    )


    try:

        result = ai_service.mark_homework(
            homework_json,
            answers
        )


    except Exception as exc:

        print(
            "SUBMIT ERROR:",
            repr(exc)
        )

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


    submission = HomeworkSubmission(
        lesson_code=lesson_code,
        student_answers=json.dumps(answers),
        score=0,
        feedback=json.dumps(result)
    )


    session.add(submission)
    session.commit()
    session.refresh(submission)


    return {
        "submission_id": submission.id,
        "result": result
    }