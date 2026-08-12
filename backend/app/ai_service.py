import json

from openai import OpenAI

from app.config import get_settings


def _text(value: object) -> str:
    return value.strip() if isinstance(value, str) else str(value).strip() if value is not None else ""


def _answer(item: dict) -> str:
    return _text(item.get("correct_answer")) or _text(item.get("answer"))


def _id_prefix(title: str) -> str:
    return {"vocabulary": "vocab", "grammar": "grammar", "reading": "reading", "writing": "writing", "challenge": "challenge"}.get(title, "question")


def _default_type(title: str) -> str:
    return {"vocabulary": "vocabulary_multiple_choice", "grammar": "grammar_multiple_choice", "reading": "true_false", "writing": "writing", "challenge": "challenge"}.get(title, "open_task")


def _is_answerable(item: dict) -> bool:
    return isinstance(item.get("options"), list) or bool(_answer(item))


def _unique_id(base: str, seen: set[str]) -> str:
    candidate, suffix = base, 2
    while candidate in seen:
        candidate = f"{base}_{suffix}"
        suffix += 1
    seen.add(candidate)
    return candidate


def _normalize_dialogue(value: object) -> list[dict[str, str]] | str:
    if isinstance(value, str):
        return value.strip()
    if not isinstance(value, list):
        return _text(value)
    result: list[dict[str, str]] = []
    for line in value:
        if isinstance(line, dict):
            text = _text(line.get("text") or line.get("sentence") or line.get("content"))
            if text:
                result.append({"speaker": _text(line.get("speaker") or line.get("role")), "text": text})
        elif _text(line):
            result.append({"speaker": "", "text": _text(line)})
    return result


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
You are an experienced English teacher, ELT materials writer,
and British Council / Cambridge-style online worksheet designer.

Create a high-quality English homework worksheet using ONLY the
uploaded lesson content.

The worksheet will be displayed on an online learning platform.
Students should be able to complete Vocabulary, Grammar and Reading
by CLICKING options. Students should NOT type answers in those three
sections.

Writing and an open-ended Challenge are the only activities that may
require typed answers.

==================================================
1. LESSON ANALYSIS
==================================================

Before creating the worksheet, silently analyse the lesson.

Identify:

- lesson topic
- CEFR level
- target vocabulary
- target grammar
- language functions
- communication goals
- situations and contexts
- important examples from the lesson

Do not output this analysis.

Use it to create the homework.

The homework must be based ONLY on the uploaded lesson.

Use:

- vocabulary taught in the lesson
- grammar taught in the lesson
- topics from the lesson
- functions from the lesson
- situations clearly connected to the lesson

Do NOT introduce unrelated grammar.

Do NOT introduce unrelated vocabulary.

Do NOT create activities simply because they are common English
activities.

The homework should feel like a natural extension of the lesson.

All content must be safe, respectful, inclusive and suitable for
English learners.

Do not include:

- sexual content
- political persuasion
- religious persuasion
- drugs
- weapons
- illegal activities
- graphic violence
- discrimination
- stereotypes
- disturbing situations
- inappropriate relationships

Use realistic everyday contexts such as:

- work
- school
- travel
- shopping
- hobbies
- technology
- family
- daily life
- community
- learning

Create exactly these five sections:

1. Vocabulary
2. Grammar
3. Reading
4. Writing
5. Challenge

The final JSON MUST have this structure:

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

Do not add additional sections.

==================================================
2. VOCABULARY
==================================================

Create ONE vocabulary multiple-choice activity.

Students MUST choose an answer.

Students MUST NOT type vocabulary answers.

Every vocabulary item MUST be a sentence in context.

The purpose is to test whether the learner understands the meaning
and use of the target vocabulary.

Create AT LEAST five vocabulary items.

Create more when necessary to cover important target vocabulary.

Do NOT create:

- isolated word questions
- vocabulary lists
- matching
- definitions
- translation
- typing questions
- paragraph gap-fill
- random sentences unrelated to the lesson

Each vocabulary item MUST contain:

- id
- sentence
- options
- answer

Each sentence MUST contain exactly ONE blank.

Each item MUST contain exactly THREE options.

Only ONE option may be correct.

All three options should come from the target vocabulary in the lesson
whenever possible.

The distractors must be meaningful and related to the same vocabulary
set.

BAD:

"She ______ her homework."

Options:

- beautiful
- quickly
- yesterday

GOOD:

"Please put the files in the ______ next to the printer."

Options:

- cupboard
- sofa
- water cooler

The vocabulary question must test meaning through context.

The sentence must make the correct answer clear.

Do not make the correct answer obvious only because it is the only
grammatically possible option. Meaning and context must help the learner.

Every vocabulary sentence must:

- be natural English
- be grammatically correct
- be appropriate for the learner level
- clearly demonstrate the vocabulary meaning
- relate to the lesson
- have exactly one possible answer

Before returning the activity, mentally test EVERY option in EVERY
sentence.

If two options could reasonably work, rewrite the sentence.

The vocabulary activity MUST use:

"type": "vocabulary_multiple_choice"

Use this exact structure:

{
  "id": "vocab_1",
  "type": "vocabulary_multiple_choice",
  "question": "Choose the correct word.",
  "items": [
    {
      "id": "vocab_1_1",
      "sentence": "Sentence with one blank.",
      "options": [
        "option 1",
        "option 2",
        "option 3"
      ],
      "answer": "correct option"
    }
  ]
}

==================================================
3. GRAMMAR
==================================================

Grammar MUST ALWAYS be a MULTIPLE-CHOICE activity.

Students MUST NEVER type grammar answers.

Students MUST ONLY choose from THREE options.

Grammar MUST ALWAYS be presented through SHORT DIALOGUES.

Do NOT create:

- ordinary isolated sentences
- gap-fill typing questions
- "Write your answer here"
- open grammar questions
- error correction requiring typing
- sentence transformation requiring typing
- paragraphs with multiple gaps

Create AT LEAST five grammar dialogue items.

Each grammar item MUST contain:

- id
- dialogue
- sentence
- options
- answer

The "dialogue" field is the MAIN grammar content.

The "sentence" field MUST contain the SAME dialogue as the
"dialogue" field.

This is required for compatibility with the online worksheet display.

Each dialogue MUST contain exactly ONE blank.

Each dialogue MUST have exactly THREE options.

Exactly ONE option must be correct.

==================================================
VERY IMPORTANT GRAMMAR DISTRACTOR RULE
==================================================

The three options MUST be plausible and related to the grammar or
language function being tested.

However, ONLY ONE option may be a natural and logically supported
completion of the dialogue.

Do NOT create distractors that are obviously silly, unrelated,
grammatically impossible, or from a completely different topic.

At the same time, do NOT create three answers that could all naturally
work.

The surrounding dialogue MUST provide enough information to eliminate
the two distractors.

The distinction between the correct answer and the distractors may
come from:

- meaning
- agreement or disagreement
- the speaker's stated opinion
- the previous sentence
- the following sentence
- tense
- subject
- number
- word form
- grammatical structure
- a clear language function

For example, if the dialogue says:

A: Let's take out the old furniture.
B: I don't think ______. It's still useful.

The options should NOT all be expressions that could naturally follow.

The context "It's still useful" should clearly support disagreement
with the suggestion.

Do NOT use three options such as:

- that's a good idea
- that's not a good idea
- I agree

because more than one may work depending on interpretation.

Instead, make the context strong enough that one answer is clearly
supported.

IMPORTANT:

Do not assume that a phrase is wrong merely because another phrase is
more natural.

For example:

"I don't think you're right about that."

and

"I don't think I agree with you."

can both be grammatical in appropriate contexts.

Therefore, if two options could reasonably work, the dialogue MUST be
rewritten until only one answer is defensible.

Before returning every grammar item, mentally test all three options
as a real English teacher.

Ask:

"Could a competent English learner reasonably argue that option 2 or
option 3 also works?"

If YES, rewrite the dialogue and/or the options.

The goal is NOT to make distractors stupid.

The goal is to make the context precise enough that only one answer is
supported.

==================================================

Each grammar dialogue MUST contain exactly ONE blank.

Each grammar item MUST have:

- exactly three options
- exactly one correct answer
- the correct answer inside the options
- meaningful distractors
- clear context

The correct answer must match:

- grammar
- meaning
- context
- language function
- subject
- number
- word form

Do not make grammar questions depend on vocabulary that was not taught.

Use realistic short conversations.

Avoid unnecessarily difficult dialogue.

The grammar activity MUST use:

"type": "grammar_multiple_choice"

The grammar question MUST be:

"Choose the correct phrase to complete each dialogue."

Use exactly this structure:

{
  "id": "grammar_1",
  "type": "grammar_multiple_choice",
  "question": "Choose the correct phrase to complete each dialogue.",
  "items": [
    {
      "id": "grammar_1_1",
      "dialogue": "A: ...\\nB: ... ______ ...",
      "sentence": "A: ...\\nB: ... ______ ...",
      "options": [
        "option 1",
        "option 2",
        "option 3"
      ],
      "answer": "correct option"
    }
  ]
}

NEVER use:

"type": "grammar_gap_fill"

NEVER create a grammar item that contains only a sentence.

NEVER create a grammar item without options.

NEVER create a grammar item that requires typing.

==================================================
4. READING
==================================================

Create ONE complete reading passage directly connected to the lesson.

The passage must:

- match the learner's CEFR level
- use target vocabulary naturally
- use target grammar naturally
- relate directly to the lesson topic
- have a realistic situation
- have a clear beginning and ending

Suitable formats include:

- dialogue
- conversation
- email
- message
- diary entry
- blog post
- short article
- interview
- review
- announcement

After the passage, create EXACTLY FIVE True/False items.

Students MUST choose True or False.

Students MUST NOT type the reading answers.

Every reading item MUST contain:

- id
- statement
- question
- options
- answer

The "statement" field contains the actual True/False statement.

The "question" field MUST contain the SAME statement.

This is required for compatibility with the existing worksheet display.

The options MUST always be:

[
  "True",
  "False"
]

The answer MUST be exactly:

"True"

or:

"False"

There MUST be both True and False answers among the five items.

==================================================
VERY IMPORTANT READING RULE
==================================================

Every reading statement MUST be directly supported or directly
contradicted by information in the passage.

Do NOT write statements about information that the passage does not
mention.

For example, if the passage says:

"They choose a round table."

Do NOT create:

"Mike thinks a square table is the best choice."

because the passage does not tell us what Mike thinks about a square
table.

Instead, create a statement that is clearly supported or contradicted
by the passage.

Each True/False statement must be answerable ONLY by reading the
passage, not by guessing or using outside knowledge.

Before returning the reading activity, check each statement against
the passage.

Ask:

"Can the student prove this answer directly from the passage?"

If the answer is NO, rewrite the statement.

Do NOT create opinion questions.

Do NOT create questions requiring outside knowledge.

Do NOT create ambiguous statements.

Use this structure:

{
  "title": "Reading",
  "passage": "Complete reading passage.",
  "questions": [
    {
      "id": "reading_1",
      "type": "reading_true_false",
      "question": "Read the passage and choose True or False.",
      "items": [
        {
          "id": "reading_1_1",
          "statement": "Statement about the passage.",
          "question": "Statement about the passage.",
          "options": [
            "True",
            "False"
          ],
          "answer": "True"
        }
      ]
    }
  ]
}

There MUST be exactly five reading items.

==================================================
5. WRITING
==================================================

Create ONE realistic writing task.

Writing is the ONLY main section where students should type a longer
answer.

The task must clearly explain:

- what to write
- who they are writing to, when appropriate
- why they are writing
- what information to include

The task must connect to:

- lesson topic
- target vocabulary
- target grammar
- communication goal

Use:

"marking_criteria"

Do NOT use:

"correct_answer"

Example:

{
  "id": "writing_1",
  "type": "writing",
  "question": "Write a short email to a friend describing your new office. Describe the furniture, say where the different things are, and explain what you like about the office.",
  "marking_criteria": [
    "Uses target vocabulary from the lesson.",
    "Uses the target grammar accurately.",
    "Includes the required information.",
    "Uses clear and organised sentences."
  ]
}

==================================================
6. CHALLENGE
==================================================

Create ONE meaningful challenge activity.

The challenge may be open-ended.

It must still use lesson content.

It must have a clear instruction.

Use:

"type": "creative_communication"

if the challenge requires an open response.

Example:

{
  "id": "challenge_1",
  "type": "creative_communication",
  "question": "Imagine you are helping a new colleague organise the office. Write a short message explaining where you would put the furniture and why.",
  "marking_criteria": [
    "Uses vocabulary from the lesson.",
    "Uses the target grammar accurately.",
    "Communicates ideas clearly."
  ]
}

==================================================
7. ANSWER KEY
==================================================

THIS IS CRITICAL FOR GRADING.

Every fixed-answer ITEM must have its own answer-key entry.

That means:

- every vocabulary item
- every grammar item
- every reading item

must have its own answer-key entry.

Use the ITEM ID, not the parent activity ID.

Correct:

{
  "id": "grammar_1_1",
  "correct_answer": "went"
}

Incorrect:

{
  "id": "grammar_1",
  "correct_answer": [...]
}

Incorrect:

{
  "id": "grammar_1"
}

For example:

[
  {
    "id": "vocab_1_1",
    "correct_answer": "photocopier"
  },
  {
    "id": "vocab_1_2",
    "correct_answer": "cupboard"
  },
  {
    "id": "grammar_1_1",
    "correct_answer": "went"
  },
  {
    "id": "grammar_1_2",
    "correct_answer": "are"
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

There MUST be five reading answer-key entries because there are exactly
five reading items.

Do NOT create answer-key entries for open-ended Writing.

Do NOT create answer-key entries for open-ended Challenge.

Never create an empty correct_answer.

Never create undefined values.

==================================================
8. FINAL VALIDATION
==================================================

Before returning JSON, check EVERYTHING below.

VOCABULARY:

- At least five items.
- Every item has a unique ID.
- Every item has exactly one sentence.
- Every sentence has exactly one blank.
- Every item has exactly three options.
- Every item has exactly one answer.
- The answer appears in the options.
- The answer is target vocabulary from the lesson.
- Distractors are related lesson vocabulary.
- The sentence clearly demonstrates meaning.
- Only one option works naturally.
- Students choose; they do not type.

GRAMMAR:

- At least five items.
- Every item has a unique ID.
- Every item is a short dialogue.
- Every dialogue has exactly one blank.
- Every item has exactly three options.
- Every item has exactly one answer.
- The answer appears in the options.
- The answer uses the grammar taught in the lesson.
- The grammar is contextual.
- Every item has BOTH "dialogue" and "sentence".
- The "sentence" field contains the SAME dialogue.
- Only one option is logically and grammatically supported.
- Distractors are plausible, not stupid.
- If two options could work, rewrite the item.
- Students choose; they never type.
- Never use grammar_gap_fill.

READING:

- Complete passage exists.
- Exactly five items.
- Every item has a unique ID.
- Every item has BOTH "statement" and "question".
- The "question" field contains the SAME statement.
- Every item has exactly two options.
- Options are exactly True and False.
- Every item has exactly one answer.
- Every answer is exactly True or False.
- Both True and False are used.
- Every statement is directly supported or contradicted by the passage.
- No statement depends on information not in the passage.
- Students choose; they never type.

WRITING:

- Exactly one task.
- The question is clear.
- The question is not empty.
- Marking criteria exist.
- No correct_answer.

CHALLENGE:

- Exactly one task.
- The question is clear.
- The question is not empty.
- Marking criteria exist if open-ended.

ANSWER KEY:

- Every vocabulary ITEM has an entry.
- Every grammar ITEM has an entry.
- Every reading ITEM has an entry.
- IDs exactly match the item IDs.
- No fixed-answer item is missing.
- No answer is undefined.
- No answer is empty.
- There are exactly five reading answer-key entries.

STRUCTURE:

- Exactly five sections.
- Correct section titles.
- Every section has a questions array.
- Reading also has a passage.
- No extra sections.
- No markdown.
- No explanations.
- Valid JSON only.

Before returning the JSON, simulate the actual student experience.

For Vocabulary:

The student sees a contextual sentence and clicks one of three
vocabulary options.

For Grammar:

The student sees a short dialogue and clicks one of three grammar
options.

For Reading:

The student reads the passage and clicks True or False for each
statement.

The student should NEVER see "Write your answer here" for Vocabulary,
Grammar or Reading.

The answer key must allow the system to mark every one of those
individual clicks.

If anything does not satisfy this experience, rewrite the activity
before returning the JSON.

Return ONLY valid JSON.

Do not return:

- Markdown
- code fences
- explanations
- comments
- notes
- undefined values
- unnecessary fields

Return the complete worksheet.
"""

        prompt = f"""
Create a homework worksheet in JSON format.

Lesson code:
{lesson_code}

Lesson content:
{lesson_text}

Return JSON only.
"""

        last_error: Exception | None = None
        for _ in range(2):
            result = self._json_request(instructions, prompt)
            try:
                normalized = self._normalize_homework(result)
                self._validate_homework_contract(normalized)
                return normalized
            except AiServiceError as exc:
                last_error = exc
        raise AiServiceError(f"OpenAI returned an incomplete worksheet after retry: {last_error}")

    # ============================================================
    # NORMALIZE AI OUTPUT
    # ============================================================

    def _normalize_homework(self, homework: dict) -> dict:
        """Return the canonical worksheet persisted, rendered and graded by the app.

        Each answerable item has one stable ID.  Existing IDs are preserved; a
        deterministic ID is created only when the model omitted one.  The
        matching answer-key entry always uses that exact same ID.
        """
        if not isinstance(homework, dict):
            raise AiServiceError("OpenAI returned an invalid homework structure.")

        raw_sections = homework.get("sections")
        if not isinstance(raw_sections, list):
            raise AiServiceError("OpenAI returned homework without valid sections.")

        canonical = {
            key: value for key, value in homework.items()
            if key not in {"sections", "answer_key"}
        }
        canonical["title"] = _text(homework.get("title")) or "Homework"
        canonical["lesson_summary"] = _text(homework.get("lesson_summary"))

        supplied_answers: dict[str, str] = {}
        raw_key = homework.get("answer_key")
        if isinstance(raw_key, list):
            for entry in raw_key:
                if not isinstance(entry, dict):
                    continue
                key = _text(entry.get("id"))
                answer = _answer(entry)
                if key and answer and key not in supplied_answers:
                    supplied_answers[key] = answer

        seen_ids: set[str] = set()
        answer_key: list[dict[str, str]] = []
        sections: list[dict] = []

        for section_index, raw_section in enumerate(raw_sections, start=1):
            if not isinstance(raw_section, dict):
                continue
            title = _text(raw_section.get("title")) or f"Section {section_index}"
            title_lower = title.lower()
            prefix = _id_prefix(title_lower)
            section = {key: value for key, value in raw_section.items() if key != "questions"}
            section["title"] = title
            if "passage" in raw_section:
                section["passage"] = _text(raw_section.get("passage"))
            questions = raw_section.get("questions")
            section["questions"] = []
            if not isinstance(questions, list):
                sections.append(section)
                continue

            for question_index, raw_question in enumerate(questions, start=1):
                if not isinstance(raw_question, dict):
                    continue
                question = dict(raw_question)
                question_id = _text(question.get("id")) or f"{prefix}_{question_index}"
                question["id"] = question_id
                question["type"] = _text(question.get("type")) or _default_type(title_lower)
                question["question"] = _text(question.get("question"))
                if isinstance(question.get("marking_criteria"), list):
                    question["marking_criteria"] = [
                        _text(value) for value in question["marking_criteria"] if _text(value)
                    ]

                raw_items = question.get("items")
                if not isinstance(raw_items, list):
                    # Some legacy model responses put one answerable item on the group.
                    raw_items = [question] if _is_answerable(question) else []
                question["items"] = []

                for item_index, raw_item in enumerate(raw_items, start=1):
                    if not isinstance(raw_item, dict):
                        continue
                    item = dict(raw_item)
                    base_id = _text(item.get("id")) or f"{question_id}_{item_index}"
                    item_id = _unique_id(base_id, seen_ids)
                    item["id"] = item_id
                    options = item.get("options")
                    item["options"] = [_text(option) for option in options if _text(option)] if isinstance(options, list) else []

                    # Preserve structured dialogue; rendering can use speaker and text.
                    if "dialogue" in item:
                        item["dialogue"] = _normalize_dialogue(item.get("dialogue"))
                    for field in ("statement", "sentence", "question", "text", "prompt", "content"):
                        if field in item:
                            item[field] = _text(item.get(field))

                    answer = _answer(item) or supplied_answers.get(item_id, "")
                    item.pop("answer", None)
                    item.pop("correct_answer", None)
                    if answer:
                        item["correct_answer"] = answer
                        answer_key.append({"id": item_id, "correct_answer": answer})
                    question["items"].append(item)

                section["questions"].append(question)
            sections.append(section)

        canonical["sections"] = sections
        canonical["answer_key"] = answer_key
        return canonical

    # ============================================================
    # JSON REQUEST
    # ============================================================

    def _validate_homework_contract(self, homework: dict) -> None:
        """Reject incomplete AI output instead of caching an options-only worksheet."""
        sections = homework.get("sections")
        if not isinstance(sections, list):
            raise AiServiceError("Worksheet has no sections.")
        by_title = {str(section.get("title", "")).lower(): section for section in sections if isinstance(section, dict)}
        grammar = by_title.get("grammar")
        reading = by_title.get("reading")
        if not grammar or not reading:
            raise AiServiceError("Worksheet must include Grammar and Reading sections.")
        grammar_items = [item for question in grammar.get("questions", []) if isinstance(question, dict) for item in question.get("items", []) if isinstance(item, dict)]
        if len(grammar_items) != 5:
            raise AiServiceError("Grammar must contain exactly five multiple-choice dialogue items.")
        for item in grammar_items:
            dialogue = item.get("dialogue")
            has_dialogue = bool(dialogue) if isinstance(dialogue, str) else isinstance(dialogue, list) and any(isinstance(line, dict) and _text(line.get("text")) for line in dialogue)
            if not has_dialogue or len(item.get("options", [])) != 3 or not _text(item.get("correct_answer")):
                raise AiServiceError("Every grammar item needs dialogue, three options, and a model answer.")
        reading_items = [item for question in reading.get("questions", []) if isinstance(question, dict) for item in question.get("items", []) if isinstance(item, dict)]
        if not _text(reading.get("passage")) or len(reading_items) != 5:
            raise AiServiceError("Reading needs a passage and exactly five True/False items.")
        answers = set()
        for item in reading_items:
            if not _text(item.get("statement")) or item.get("options") != ["True", "False"] or _text(item.get("correct_answer")) not in {"True", "False"}:
                raise AiServiceError("Every reading item needs a statement, True/False options, and a model answer.")
            answers.add(item["correct_answer"])
        if answers != {"True", "False"}:
            raise AiServiceError("Reading must include both True and False model answers.")

    def _json_request(
        self,
        instructions: str,
        user_input: str,
    ) -> dict:

        if not self.client:
            raise AiServiceError(
                "OpenAI API key is not configured."
            )

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

            raise AiServiceError(
                str(exc)
            ) from exc

        output = response.output_text.strip()

        print(
            "\n========== OPENAI RESPONSE ==========\n"
        )

        print(output)

        print(
            "\n=====================================\n"
        )

        try:

            return json.loads(output)

        except json.JSONDecodeError:

            if output.startswith("```"):

                lines = output.splitlines()

                if (
                    lines
                    and lines[0].startswith("```")
                ):
                    lines = lines[1:]

                if (
                    lines
                    and lines[-1].startswith("```")
                ):
                    lines = lines[:-1]

                output = "\n".join(
                    lines
                ).strip()

            try:

                return json.loads(output)

            except Exception as exc:

                raise AiServiceError(
                    "OpenAI returned invalid JSON:\n\n"
                    + output
                ) from exc

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

        answer_key = homework.get(
            "answer_key",
            [],
        )

        # --------------------------------------------------------
        # Build direct answer lookup.
        #
        # Example:
        #
        # vocab_1_1   -> photocopier
        # grammar_1_1 -> went
        # reading_1_1 -> True
        # --------------------------------------------------------

        answer_lookup = {}

        for item in answer_key:

            if not isinstance(item, dict):
                continue

            question_id = item.get("id")

            if not question_id:
                continue

            if "correct_answer" not in item:
                continue

            answer_lookup[
                question_id
            ] = item["correct_answer"]

        # --------------------------------------------------------
        # Find open-ended questions.
        # --------------------------------------------------------

        open_questions = {}

        for section in homework.get(
            "sections",
            [],
        ):

            if not isinstance(section, dict):
                continue

            for question in section.get(
                "questions",
                [],
            ):

                if not isinstance(question, dict):
                    continue

                question_type = question.get(
                    "type"
                )

                if question_type in [
                    "writing",
                    "creative_communication",
                ]:

                    question_id = question.get(
                        "id"
                    )

                    if not question_id:
                        continue

                    open_questions[
                        question_id
                    ] = {
                        "question": question.get(
                            "question",
                            "",
                        ),
                        "marking_criteria": question.get(
                            "marking_criteria",
                            [],
                        ),
                    }

        # --------------------------------------------------------
        # Mark submitted answers.
        # --------------------------------------------------------

        for question_id, student_answer in (
            student_answers.items()
        ):

            # ----------------------------------------------------
            # Open-ended questions
            # ----------------------------------------------------

            if question_id in open_questions:

                feedback = self.check_open_question(
                    open_questions[
                        question_id
                    ],
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

            correct_answer = answer_lookup[
                question_id
            ]

            student_value = (
                ""
                if student_answer is None
                else str(student_answer).strip()
            )

            correct_value = (
                ""
                if correct_answer is None
                else str(correct_answer).strip()
            )

            is_correct = (
                student_value.lower()
                == correct_value.lower()
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
    # CHECK OPEN QUESTION
    # ============================================================

    def check_open_question(
        self,
        task: dict,
        student_answer: str,
    ) -> dict:

        instructions = """
You are an experienced English teacher marking student writing.

Evaluate the student's answer using the task requirements and
marking criteria.

Give supportive, concise and useful feedback.

Do not give a score.

Return JSON only.

Use exactly this structure:

{
  "strengths": [
    "Positive point"
  ],
  "areas_to_improve": [
    "Specific improvement"
  ],
  "teacher_comment": "Short encouraging teacher comment"
}

Do not add any other fields.
"""

        prompt = f"""
Task:

{task.get("question", "")}

Marking criteria:

{json.dumps(
    task.get(
        "marking_criteria",
        [],
    ),
    indent=2,
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