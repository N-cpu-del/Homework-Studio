import json

from openai import OpenAI

from app.config import get_settings


class AiServiceError(Exception):
    pass


class AiService:

    def __init__(self) -> None:
        self.settings = get_settings()

        self.client = (
            OpenAI(api_key=self.settings.openai_api_key)
            if self.settings.openai_api_key
            else None
        )

    # ============================================================
    # GENERATE HOMEWORK
    # ============================================================

    def generate_homework(
        self,
        lesson_code: str,
        lesson_text: str,
    ) -> dict:

        if not self.client:
            raise AiServiceError(
                "OpenAI API key is not configured."
            )

        instructions = """
You are an experienced English teacher and professional ELT materials writer.

Create a high-quality online English homework worksheet ONLY from the uploaded lesson.

The worksheet must be:
- accurate
- natural
- communicative
- realistic
- suitable for the lesson CEFR level
- suitable for online learning
- professionally designed like a Cambridge, British Council, Oxford or Pearson coursebook activity

IMPORTANT:
Use ONLY vocabulary, grammar, topics, situations and language functions taught in the lesson.

Do not introduce unrelated grammar or vocabulary.

The worksheet must contain exactly these sections:

1. Vocabulary
2. Grammar
3. Reading
4. Writing
5. Challenge

Return ONLY valid JSON.

============================================================
VOCABULARY
============================================================

Create ONE vocabulary multiple-choice activity.

Students must choose the correct vocabulary item in CONTEXT.

DO NOT show isolated vocabulary words.

DO NOT ask students to match words with definitions.

DO NOT use vocabulary lists.

DO NOT use translation.

Every vocabulary question must be a complete natural sentence with one blank.

Example:

"Could you put the files on the _______ next to the printer?"

Options:
- desk
- sofa
- lamp

The correct answer must be a target vocabulary item from the lesson.

Create AT LEAST FIVE questions.

Use important target vocabulary from the lesson.

Each question must contain exactly THREE options.

All three options should come from the target vocabulary in the lesson whenever possible.

The options should be related to the same vocabulary topic.

The sentence must make the correct answer clear from context.

Only ONE option should be correct.

Use this structure:

{
  "id": "vocab_1",
  "type": "vocabulary_multiple_choice",
  "question": "Choose the correct word.",
  "items": [
    {
      "id": "vocab_1_1",
      "sentence": "Complete natural sentence with one blank.",
      "options": [
        "option 1",
        "option 2",
        "option 3"
      ],
      "correct_answer": "option 1"
    }
  ]
}

IMPORTANT:

Each vocabulary item MUST have:
- id
- sentence
- options
- correct_answer

The correct_answer MUST exactly match one of the options.

============================================================
GRAMMAR
============================================================

Create grammar practice using ONLY grammar taught in the lesson.

IMPORTANT:

Grammar must ALWAYS be presented as a SHORT DIALOGUE.

Students must choose the correct answer from THREE OPTIONS.

Students must NOT type grammar answers.

Do NOT create:
- open gap fills
- "write the correct form"
- base-form prompts such as "(go)"
- questions where students have to type an answer

Each grammar question should look like this:

A: "What did you do yesterday?"
B: "I _______ to the cinema with my friends."

Options:
- go
- went
- going

Correct answer:
- went

Create AT LEAST FIVE grammar questions.

Each question must contain:
- a realistic short dialogue
- one gap
- exactly three options
- one correct answer

The grammar must be contextual and connected to the lesson.

Use the grammar actually taught in the lesson.

Each grammar item must have:

{
  "id": "grammar_1_1",
  "dialogue": [
    {
      "speaker": "A",
      "text": "What did you do yesterday?"
    },
    {
      "speaker": "B",
      "text": "I _______ to the cinema."
    }
  ],
  "options": [
    "go",
    "went",
    "going"
  ],
  "correct_answer": "went"
}

The correct answer MUST exactly match one of the three options.

There must be ONLY ONE possible correct answer.

============================================================
READING
============================================================

Create ONE realistic reading passage connected directly to the lesson.

The reading should:
- match the learner level
- recycle target vocabulary
- recycle target grammar
- have a clear situation
- be natural and realistic
- feel like a real coursebook text

Suitable formats include:
- dialogue
- email
- message
- diary
- short article
- blog post
- interview
- review
- announcement

After the passage, create EXACTLY FIVE True/False statements.

Students should choose True or False.

They should NOT write open answers.

Use this structure:

{
  "title": "Reading",
  "passage": "Complete reading passage.",
  "questions": [
    {
      "id": "reading_1",
      "type": "true_false",
      "question": "Read the passage and choose True or False.",
      "items": [
        {
          "id": "reading_1_1",
          "statement": "Statement about the passage.",
          "options": [
            "True",
            "False"
          ],
          "correct_answer": "True"
        }
      ]
    }
  ]
}

There must be exactly five reading items.

Every reading item MUST contain:
- id
- statement
- options
- correct_answer

correct_answer MUST be exactly:
"True"
or
"False"

Make sure the statements include both True and False answers.

============================================================
WRITING
============================================================

Create ONE realistic writing task.

The task must:
- clearly tell the student what to write
- connect to the lesson
- use the lesson vocabulary
- use the lesson grammar
- have a realistic communication purpose

Use:

{
  "id": "writing_1",
  "type": "writing",
  "question": "Clear and specific writing instruction.",
  "marking_criteria": [
    "criterion 1",
    "criterion 2",
    "criterion 3"
  ]
}

Do NOT include correct_answer for writing.

============================================================
CHALLENGE
============================================================

Create ONE meaningful challenge task connected to the lesson.

It may be:
- creative communication
- language transformation
- correcting mistakes
- applying vocabulary
- solving a communication situation

The task must have a clear question.

For open challenge tasks use:

{
  "id": "challenge_1",
  "type": "creative_communication",
  "question": "Clear task instruction.",
  "marking_criteria": [
    "criterion 1",
    "criterion 2"
  ]
}

Do NOT include correct_answer for open challenge tasks.

============================================================
ANSWER KEY
============================================================

This is VERY IMPORTANT.

Create a separate answer_key.

The answer_key MUST contain the answers for:

- every vocabulary item
- every grammar item
- every reading item

DO NOT leave grammar out.

DO NOT leave reading out.

DO NOT include writing in the answer_key.

DO NOT include open-ended challenge tasks in the answer_key.

Use the exact individual item IDs.

Example:

[
  {
    "id": "vocab_1_1",
    "correct_answer": "desk"
  },
  {
    "id": "vocab_1_2",
    "correct_answer": "printer"
  },
  {
    "id": "grammar_1_1",
    "correct_answer": "went"
  },
  {
    "id": "grammar_1_2",
    "correct_answer": "was"
  },
  {
    "id": "reading_1_1",
    "correct_answer": "True"
  },
  {
    "id": "reading_1_2",
    "correct_answer": "False"
  }
]

IMPORTANT:

Every fixed-answer item MUST have its own answer_key entry.

The ID in answer_key MUST exactly match the ID of the question item.

============================================================
QUALITY CONTROL
============================================================

Before returning the JSON, check:

VOCABULARY:
- At least 5 questions.
- Every question is a contextual sentence.
- Every question has exactly 3 options.
- Exactly one option is correct.
- Correct answer is from lesson vocabulary.
- No isolated word questions.

GRAMMAR:
- At least 5 questions.
- Every question is a dialogue.
- Every question has one gap.
- Every question has exactly 3 options.
- Students choose an answer; they never type one.
- Exactly one answer is correct.
- Grammar matches the lesson.

READING:
- One complete passage.
- Exactly 5 True/False items.
- Each has True and False as options.
- Each has a correct_answer.
- Reading answers are included in answer_key.

WRITING:
- Clear instruction.
- Connected to lesson.
- Has marking_criteria.
- No correct_answer.

CHALLENGE:
- Clear instruction.
- Connected to lesson.

ANSWER KEY:
- Vocabulary included.
- Grammar included.
- Reading included.
- Writing excluded.
- Open challenge excluded.
- Every fixed-answer item has an answer_key entry.

Return ONLY valid JSON.

The final JSON MUST have exactly this top-level structure:

{
  "lesson_summary": "",
  "title": "",
  "sections": [
    {
      "title": "Vocabulary",
      "questions": []
    },
    {
      "title": "Grammar",
      "questions": []
    },
    {
      "title": "Reading",
      "passage": "",
      "questions": []
    },
    {
      "title": "Writing",
      "questions": []
    },
    {
      "title": "Challenge",
      "questions": []
    }
  ],
  "answer_key": []
}
"""

        prompt = f"""
Create a homework worksheet in JSON format.

Lesson code:
{lesson_code}

Lesson content:
{lesson_text}

Return JSON only.
"""

        return self._json_request(
            instructions,
            prompt,
        )

    # ============================================================
    # OPENAI JSON REQUEST
    # ============================================================

    def _json_request(
        self,
        instructions: str,
        user_input: str,
    ) -> dict:

        try:
            response = self.client.responses.create(
                model=self.settings.openai_model,
                instructions=instructions,
                input=user_input,
                text={
                    "format": {
                        "type": "json_object"
                    }
                },
            )

        except Exception as exc:
            raise AiServiceError(str(exc)) from exc

        output = response.output_text.strip()

        print("\n========== OPENAI RESPONSE ==========\n")
        print(output)
        print("\n=====================================\n")

        try:
            return json.loads(output)

        except json.JSONDecodeError:

            if output.startswith("```"):

                lines = output.splitlines()

                if lines and lines[0].startswith("```"):
                    lines = lines[1:]

                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]

                output = "\n".join(lines).strip()

            try:
                return json.loads(output)

            except Exception:
                raise AiServiceError(
                    f"OpenAI returned invalid JSON:\n\n{output}"
                )

    # ============================================================
    # MARK HOMEWORK
    # ============================================================

    def mark_homework(
        self,
        homework: dict,
        student_answers: dict,
    ) -> dict:

        results = []
        writing_feedback = []

        answer_key = homework.get("answer_key", [])

        # --------------------------------------------------------
        # Build answer lookup
        # --------------------------------------------------------

        answer_lookup = {}

        for item in answer_key:

            question_id = item.get("id")

            if not question_id:
                continue

            correct = item.get("correct_answer")

            answer_lookup[question_id] = correct

        # --------------------------------------------------------
        # Find open-ended questions
        # --------------------------------------------------------

        open_questions = {}

        for section in homework.get("sections", []):

            for question in section.get("questions", []):

                question_type = question.get("type")

                if question_type in [
                    "writing",
                    "creative_communication",
                ]:

                    open_questions[question["id"]] = {
                        "question": question.get(
                            "question",
                            ""
                        ),
                        "marking_criteria": question.get(
                            "marking_criteria",
                            []
                        ),
                    }

        # --------------------------------------------------------
        # Mark student answers
        # --------------------------------------------------------

        for question_id, student_answer in student_answers.items():

            # ----------------------------------------------------
            # Open-ended questions
            # ----------------------------------------------------

            if question_id in open_questions:

                feedback = self.check_open_question(
                    open_questions[question_id],
                    student_answer,
                )

                writing_feedback.append({
                    "id": question_id,
                    "student_answer": student_answer,
                    "feedback": feedback,
                })

                continue

            # ----------------------------------------------------
            # Fixed-answer questions
            # ----------------------------------------------------

            if question_id not in answer_lookup:
                continue

            correct_answer = answer_lookup[question_id]

            # ----------------------------------------------------
            # If the student answer is a dictionary
            # ----------------------------------------------------

            if isinstance(student_answer, dict):

                item_results = {}
                correct_details = {}

                for number, answer in correct_answer.items():

                    student_value = student_answer.get(
                        number,
                        ""
                    )

                    is_correct = (
                        str(student_value).strip().lower()
                        ==
                        str(answer).strip().lower()
                    )

                    item_results[number] = is_correct
                    correct_details[number] = answer

                results.append({
                    "id": question_id,
                    "correct": all(
                        item_results.values()
                    ),
                    "student_answer": student_answer,
                    "correct_answer": correct_details,
                    "details": item_results,
                })

                continue

            # ----------------------------------------------------
            # Normal single-answer question
            # ----------------------------------------------------

            is_correct = (
                str(student_answer).strip().lower()
                ==
                str(correct_answer).strip().lower()
            )

            results.append({
                "id": question_id,
                "correct": is_correct,
                "student_answer": student_answer,
                "correct_answer": correct_answer,
            })

        return {
            "results": results,
            "writing_feedback": writing_feedback,
        }

    # ============================================================
    # AI MARKING FOR WRITING / CHALLENGE
    # ============================================================

    def check_open_question(
        self,
        task: dict,
        student_answer: str,
    ) -> dict:

        instructions = """
You are an experienced English teacher marking student writing.

Evaluate the student's answer using the task requirements and marking criteria.

Give supportive, concise and useful feedback.

Do not give a score.

Return JSON only:

{
  "strengths": [
    "Positive point"
  ],
  "areas_to_improve": [
    "Specific improvement"
  ],
  "teacher_comment": "Short encouraging teacher comment"
}
"""

        prompt = f"""
Task:

{task.get("question", "")}

Marking criteria:

{json.dumps(
    task.get("marking_criteria", []),
    indent=2
)}

Student answer:

{student_answer}

Evaluate:

- task completion
- grammar accuracy
- vocabulary use
- clarity
- organisation

Return JSON only.
"""

        return self._json_request(
            instructions,
            prompt,
        )

    # ============================================================
    # BACKWARD COMPATIBILITY
    # ============================================================

    def check_writing(
        self,
        task: dict,
        student_answer: str,
    ) -> dict:

        return self.check_open_question(
            task,
            student_answer,
        )