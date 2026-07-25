from typing import Literal

from pydantic import BaseModel, Field


SectionName = Literal[
    "Vocabulary",
    "Grammar",
    "Reading",
    "Writing",
]

QuestionType = Literal[
    "matching",
    "gap_fill",
    "sentence_completion",
    "multiple_choice",
    "correct_mistake",
    "rewrite",
    "true_false",
    "reading_question",
    "writing",
]


class Question(BaseModel):
    id: str
    section: SectionName
    type: QuestionType
    prompt: str

    # Used for multiple choice questions
    options: list[str] = Field(default_factory=list)

    # Correct answer for automatic marking
    answer: str

    points: int = Field(default=1, ge=1, le=10)


class HomeworkContent(BaseModel):
    title: str = "Homework"

    lesson_code: str

    vocabulary: list[Question]

    grammar: list[Question]

    reading_text: str

    reading_questions: list[Question]

    writing_task: Question


class GenerateHomeworkRequest(BaseModel):
    lesson_code: str


class CreateLessonResponse(BaseModel):
    lesson_code: str
    message: str


class StudentHomeworkResponse(BaseModel):
    lesson_code: str
    homework: HomeworkContent


class StudentAnswer(BaseModel):
    question_id: str
    answer: str


class SubmitHomeworkRequest(BaseModel):
    lesson_code: str
    answers: list[StudentAnswer]


class QuestionResult(BaseModel):
    question_id: str

    correct: bool

    correct_answer: str | None = None


class WritingFeedback(BaseModel):
    score: int = Field(ge=0, le=10)

    mistakes: list[str] = Field(default_factory=list)


class SubmitHomeworkResponse(BaseModel):
    score: int

    total_points: int

    question_results: list[QuestionResult]

    writing_feedback: WritingFeedback | None = None


class LessonDashboardItem(BaseModel):
    lesson_code: str

    students_opened: int

    students_submitted: int


class TeacherLoginRequest(BaseModel):
    access_code: str


class TeacherLoginResponse(BaseModel):
    success: bool


class SettingsUpdateRequest(BaseModel):
    delete_after_days: int = Field(
        default=7,
        ge=1,
        le=365,
    )