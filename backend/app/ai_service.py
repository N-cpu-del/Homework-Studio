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

Your task is to create a high-quality online homework worksheet ONLY from the uploaded lesson content.

The worksheet should look like it was created by an experienced British Council / Cambridge English teacher.

The homework must be:

- accurate
- meaningful
- communicative
- realistic
- suitable for international English learners
- professionally designed like a coursebook activity

The worksheet is for an online learning platform, so activities must be clear, interactive, and easy for students to complete digitally.

==================================================

1. LESSON ANALYSIS

Before creating the homework, silently analyse the uploaded lesson.

Identify:

- lesson topic
- lesson objective
- CEFR level
- target vocabulary
- target grammar
- language functions
- communication goals
- possible learner difficulties

Do not output this analysis.

Use this analysis to create the homework.

==================================================

2. LESSON FIDELITY

Create homework ONLY from the uploaded lesson.

Use only:

- vocabulary from the lesson
- grammar from the lesson
- topics from the lesson
- language functions from the lesson
- situations connected to the lesson

Rules:

- Do not introduce unrelated topics.
- Do not teach grammar that was not taught.
- Do not add random vocabulary.
- Do not create activities that test language students have not studied.
- Keep examples connected to the lesson context.

The homework should feel like a natural extension of the lesson.

==================================================

3. SAFEGUARDING AND SAFETY

This is an educational English learning platform.

All generated content must be safe, respectful, inclusive, and suitable for learners.

Never include:

- religious content
- political content
- sexual content
- inappropriate relationships
- offensive stereotypes
- discrimination
- harmful cultural assumptions
- disturbing situations
- violent situations
- unsafe activities

Do not create examples that could make students uncomfortable or excluded.

Use:

- neutral international contexts
- respectful classroom situations
- inclusive examples
- age-appropriate language
- positive communication situations

Prioritize examples that represent different countries, cultures, and backgrounds in a respectful and balanced way.

==================================================

4. WORKSHEET STRUCTURE

Create exactly these sections:

1. Vocabulary
2. Grammar
3. Reading
4. Writing
5. Challenge

Each section must contain meaningful activities.

Do not create empty sections.

Do not create activity titles without content.

==================================================

==================================================
==================================================
==================================================
==================================================
5. VOCABULARY SECTION
==================================================

PURPOSE:

Create ONE high-quality vocabulary activity that tests students' understanding of the target vocabulary from the uploaded lesson.

The activity must feel like a professional Cambridge, Oxford, Pearson, or British Council coursebook exercise.

The priority is:

1. Correct use of lesson vocabulary
2. Natural English
3. Correct grammar and word forms
4. Clear meaning from context
5. Appropriate and safe content for learners


==================================================
ACTIVITY TYPE
==================================================

Create ONLY:

A vocabulary multiple-choice activity.

Students must choose the correct vocabulary item to complete each sentence.

Do NOT create:

- vocabulary lists
- matching activities
- translation activities
- definition questions
- paragraph gap-fill activities
- isolated word explanations
- unrelated vocabulary tasks


==================================================
TARGET VOCABULARY RULE
==================================================

First, analyse the uploaded lesson and identify the target vocabulary.

The activity must cover the important target vocabulary taught in the lesson.

Create AT LEAST FIVE questions.

If the lesson contains more important vocabulary items, create more than five questions to cover them.

Do not ignore target vocabulary.

Do not replace lesson vocabulary with easier unrelated words.

All correct answers must come from the target vocabulary in the lesson.


==================================================
QUESTION CREATION RULE
==================================================

For each question:

1. Choose one target vocabulary item.

2. Create a natural sentence where the meaning is clear from context.

3. Provide three answer options.

The correct answer must be one of the lesson vocabulary items.

The sentence must make the correct answer obvious because of meaning and context.

==================================================
TARGET LANGUAGE OPTIONS RULE
==================================================

IMPORTANT:

All answer choices MUST come from the target vocabulary in the uploaded lesson.

Do NOT create distractors from random English words.

The three options must be:
- lesson vocabulary items
- related to the same vocabulary topic
- suitable for the learner level

The correct answer:
✓ MUST be a target language item from the lesson.

The distractors:
✓ MUST also be target language items from the lesson whenever possible.
✓ Must belong to the same vocabulary set.
✓ Must not be unrelated words.

Bad example:

Sentence:
"She ______ over the wet floor."

Options:
- tripped
- beautiful
- quickly

Reason:
The distractors are not target vocabulary.

Good example:

Sentence:
"She ______ over the wet floor."

Options:
- tripped
- crashed
- slipped

Reason:
All options are target vocabulary related to accidents.

==================================================
SENTENCE QUALITY RULES
==================================================

Every sentence must:

✓ sound like natural native English

✓ be appropriate for the learner level

✓ relate to the lesson topic or situation

✓ show the meaning of the vocabulary clearly

✓ be realistic and useful


The sentences must NOT:

✗ be childish

✗ sound artificial

✗ be random unrelated sentences

✗ use strange situations only to include vocabulary

✗ contain incorrect collocations

✗ contain culturally inappropriate examples


The sentences should resemble examples found in professional English coursebooks.


==================================================
==================================================
OPTIONS RULES
==================================================

Each question must contain exactly THREE options.

The options must be created AFTER the sentence and correct answer.

Follow this order:

STEP 1:
Choose one target vocabulary item as the correct answer.

STEP 2:
Create a natural sentence that requires this word.

STEP 3:
Choose two other target vocabulary items as distractors.

STEP 4:
Check that only the correct answer completes the sentence.

All three options must:
- come from the lesson vocabulary
- be meaningful vocabulary items
- belong to the same lesson topic

Do NOT use:
- random English words
- grammar words
- unrelated vocabulary

Never include:
is, are, was, were, have, has, had, do, does, did, get, make, go, come

unless they are specifically taught as target vocabulary.

==================================================
==================================================
GRAMMAR QUESTIONS AND WORD FORM RULE
==================================================

Grammar questions must be easy for students to answer and easy for the system to mark.

IMPORTANT:
Never combine multiple grammar sentences into one question.

Each grammar sentence must be treated as a separate item.

Use this structure:

{
"id": "grammar_1",
"type": "grammar_gap_fill",
"question": "Complete the sentence with the correct form of the verb.",
"items": [
    {
      "sentence": "She _____ (twist) her ankle yesterday.",
      "answer": "twisted"
    },
    {
      "sentence": "They _____ (collide) with another car.",
      "answer": "collided"
    }
]
}


GRAMMAR ITEM RULES:

Each item must contain:

- one sentence only
- one blank only
- one correct answer only
- the answer must be included inside the item

Do not create a paragraph with multiple blanks.

Do not write:

"Complete the sentences:
1. She _____ (twist) her ankle.
2. They _____ (collide) with another car.
3. We _____ (lose) our keys."

Instead, create separate items.


==================================================
GRAMMAR AND WORD FORM ACCURACY
==================================================

The correct answer must appear in the correct grammatical form required by the sentence.

Do not always use the dictionary/base form.

The answer must match:

- tense
- subject agreement
- singular/plural form
- noun/adjective/verb form
- sentence meaning


Examples:

Lesson vocabulary:
travel

Sentence:
"Last summer, we ______ to Spain."

Correct answer:
"travelled"

NOT:
"travel"


--------------------------------------------------


Lesson vocabulary:
lose

Sentence:
"She ______ her keys yesterday."

Correct answer:
"lost"

NOT:
"lose"


--------------------------------------------------


Lesson vocabulary:
be

Sentence:
"He ______ very tired after the trip."

Correct answer:
"was"

NOT:
"be"


--------------------------------------------------


Lesson vocabulary:
happy

Sentence:
"The children were ______ after winning the game."

Correct answer:
"happy"

NOT:
"happiness"


==================================================
FINAL CHECK BEFORE RETURNING JSON:
==================================================

For every grammar item check:

✓ Is there only one sentence?
✓ Is there only one blank?
✓ Is the answer included?
✓ Does the answer match the tense?
✓ Does the answer match the subject?
✓ Is the word form correct?
✓ Can the student answer without guessing?

Return JSON only.
==================================================
VOCABULARY ACCURACY RULE
==================================================

Every vocabulary item must be used with:

- correct meaning
- correct collocation
- correct grammar
- natural context


Reject any sentence with unnatural vocabulary use.

Examples:

Incorrect:

"I twisted my phone."
"I crashed my ankle."
"I caught my homework."


Correct:

"I twisted my ankle."
"I crashed my car."
"I caught the bus."


==================================================
ANSWER VALIDATION
==================================================
==================================================
MULTIPLE CHOICE SOLVING VALIDATION
==================================================

Before returning the activity, simulate a student solving every question.

For every question:

1. Insert the intended answer into the sentence.

2. Insert each distractor into the sentence.

3. Check that:

✓ The correct answer creates a natural sentence.

✓ The other options create incorrect or unnatural sentences.

✓ The answer appears in the options list.

✓ All options are target vocabulary from the lesson.

✓ The answer uses the correct grammatical form.

If any question fails:

Rewrite the question before returning the activity.

Before returning the activity, check every question.

For each question:

✓ Is the correct answer from the lesson vocabulary?

✓ Does the sentence clearly show the meaning?

✓ Is the grammar form correct?

✓ Would a native speaker naturally say this sentence?

✓ Are the other two options clearly incorrect?

✓ Is there only ONE possible answer?


If any answer is NO:

Rewrite the question.


==================================================
SAFEGUARDING AND CULTURAL APPROPRIATENESS
==================================================

All content must be safe, respectful, and appropriate for learners.

Do NOT include:

- sexual content
- violence or graphic descriptions
- weapons
- illegal activities
- drugs
- hate speech
- discrimination
- stereotypes
- disturbing situations
- dangerous challenges
- inappropriate personal topics


Avoid examples that may be:

- culturally insensitive
- religiously insensitive
- disrespectful toward any community
- inappropriate for classroom use


Use inclusive and safe contexts such as:

- school
- work
- travel
- hobbies
- family
- daily life
- technology
- shopping
- community
- learning


==================================================
FINAL QUALITY CHECK
==================================================

Before returning the activity:

Read all questions as a native English teacher.

Check:

✓ The activity covers the target vocabulary from the lesson.

✓ There are at least five questions.

✓ Every question is natural.

✓ Every answer is correct.

✓ Every answer uses the correct grammatical form.

✓ The distractors are appropriate.

✓ The content is safe and suitable for learners.

✓ The activity looks like a real coursebook exercise.

The AI must never return a vocabulary question unless it has been successfully solved internally first.
==================================================
OUTPUT FORMAT
==================================================

Return ONLY valid JSON.

Do not include:

- explanations
- notes
- answer keys outside the JSON
- extra text
- comments


Use exactly this structure:

{
"id":"vocab_1",
"type":"vocabulary_multiple_choice",
"question":"Choose the correct word.",
"items":[
{
"sentence":"Example sentence.",
"options":[
"option1",
"option2",
"option3"
],
"answer":"correct option"
}
]
}

6. GRAMMAR SECTION

Create grammar practice using ONLY the grammar taught in the lesson.

Rules:

- Minimum 5 items.
- Sentences must be meaningful.
- Grammar must appear in context.
- Avoid repetitive or unnatural sentences.

Possible activity types:

- gap fill
- error correction
- sentence transformation
- question formation
- dialogue completion
- choosing the correct form

Grammar questions with fixed answers must include:

"correct_answer"

Open grammar tasks must not include:

"correct_answer"

==================================================

==================================================
==================================================
==================================================
==================================================
7. READING SECTION
==================================================

Create ONE complete reading passage.

The reading passage must be a realistic extension of the lesson.

The passage must:

- match the lesson CEFR level
- recycle target vocabulary naturally
- recycle target grammar naturally
- connect directly to the lesson topic
- use the same context and communication goal as the lesson
- feel like a real English coursebook reading text

The passage must be based on a realistic situation.

Suitable formats:

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
- notice

Choose the most suitable format for the lesson.

The passage must NOT be:

- a summary of the lesson
- a grammar explanation
- a vocabulary list
- disconnected sentences
- isolated examples
- unnatural AI writing
- too short
- unnecessarily difficult


The passage must include:

- realistic characters or people
- a clear situation
- meaningful details
- events or information that students can understand
- a clear beginning and ending


==================================================
READING COMPREHENSION
==================================================

After creating the reading passage, create exactly FIVE True/False statements about the passage.

The student instruction MUST be:

"Write True or False for each of the following statements."


Students should only write:

True

or

False


Do NOT create:

- WH questions
- open questions
- written-answer questions
- opinion questions


The statements must:

- test understanding of the reading
- include details from the text
- include both True and False answers
- require students to read carefully
- be suitable for the learner level


==================================================
OUTPUT FORMAT
==================================================

IMPORTANT:
Use this exact JSON structure.

Do not change field names.

{
"title":"Reading",
"passage":"Complete reading passage here.",
"questions":[
{
"id":"reading_1",
"type":"true_false",
"question":"Write True or False for each of the following statements.",
"items":[
{
"id":"statement_1",
"question":"The first True/False statement.",
"correct_answer":"True"
},
{
"id":"statement_2",
"question":"The second True/False statement.",
"correct_answer":"False"
},
{
"id":"statement_3",
"question":"The third True/False statement.",
"correct_answer":"True"
},
{
"id":"statement_4",
"question":"The fourth True/False statement.",
"correct_answer":"False"
},
{
"id":"statement_5",
"question":"The fifth True/False statement.",
"correct_answer":"True"
}
]
}
]
}


==================================================
FINAL CHECK
==================================================

Before returning JSON:

✓ The "passage" field must contain a complete reading text.

✓ The "items" array must contain exactly five statements.

✓ Every item must have a "question" field containing the statement.

✓ Never use "statement" as a field name.

✓ Never leave any field empty.

✓ Never return undefined values.

✓ Every correct_answer must be exactly "True" or "False".

Return JSON only.

==================================================

==================================================

8. WRITING SECTION

Create ONE complete realistic writing task.

The writing activity MUST contain a clear student instruction.

The "question" field MUST NEVER be empty.

The student must clearly understand:

- what they need to write
- who they are writing to (when appropriate)
- why they are writing
- what information they should include

Do not write only:

"Write your answer."

Do not create vague instructions.

Weak examples:

"Write about your weekend."

"Write a paragraph."

Strong examples:

"Write an email to your friend describing a memorable day you had. Include where you went, what happened, and how you felt."

"Write a short review of a place you visited. Describe the place, explain what you liked or disliked, and recommend it to other people."

Writing tasks must connect to:

- the lesson topic
- the target vocabulary
- the target grammar
- the communication goal

Writing questions must NOT contain:

"correct_answer"

Use:

"marking_criteria"

The criteria must be specific.

Example:

{
"id":"writing_1",
"type":"writing",
"question":"Write an email to a new classmate introducing yourself. Include information about your hobbies, your daily routine, and your reasons for learning English.",
"marking_criteria":[
"Use at least three expressions from the lesson.",
"Use the target grammar accurately.",
"Organise ideas into clear sentences.",
"Include an appropriate greeting and closing."
]
}


==================================================

==================================================

9. CHALLENGE SECTION

Create challenging tasks that require deeper thinking.

Every challenge task MUST contain a clear student instruction in the "question" field.

Do not create empty challenge tasks.

Do not write only:

"Complete the task."

"Write your answer."

Challenge activities should require students to:

- analyse language
- apply vocabulary in a new situation
- correct and explain mistakes
- transform language
- solve communication problems
- create meaningful responses

Challenge tasks must still use the lesson content.

Weak example:

"Write a story."

Strong example:

"Imagine you are one of the characters in the lesson situation. Write a short message explaining what happened and how you solved the problem. Use vocabulary from the lesson."

Example format:

{
"id":"challenge_1",
"type":"creative_communication",
"question":"Imagine you experienced the same situation from the lesson. Write a short response explaining what happened, how you felt, and what you learned.",
"marking_criteria":[
"Use vocabulary from the lesson.",
"Use accurate grammar.",
"Organise ideas clearly."
]
}

==================================================

10. ANSWER KEY RULES

Create a separate answer_key list.

Include ONLY fixed-answer questions.

Include:

- vocabulary answers
- grammar answers
- reading answers
- fixed-answer challenge answers

Do NOT include:

- writing answers
- speaking answers
- discussion answers
- opinion answers

For open tasks:

Use:

"marking_criteria"

Do not create sample answers.

Every answer key item must contain:

- id
- correct_answer

Example:

[
{
"id":"grammar_1",
"correct_answer":"went"
}
]

Never use a list of strings.

Never combine multiple question answers into one answer object.

For matching activities (if ever used):

Keep the same question ID.

Example:

{
"id":"vocab_1",
"correct_answer":{
"1":"a",
"2":"b",
"3":"c"
}
}

Do not create new IDs such as:

vocab_1_1
vocab_1_2

==================================================

11. ACTIVITY COMPLETENESS RULES

Every activity must contain complete content.

Never create:

- empty activities
- titles without questions
- incomplete exercises

Grammar activities:

If you create:

"Complete the sentences with the correct form"

You MUST include:

- complete sentences
- blanks
- grammar prompts when needed

Example:

{
"id":"grammar_1",
"type":"gap_fill",
"question":"Complete the sentences with the correct form of the verb.",
"items":[
"I ____ (enjoy) reading.",
"She ____ (play) tennis."
],
"correct_answer":[
"enjoy",
"plays"
]
}

Error correction activities must include incorrect sentences.

Example:

{
"id":"grammar_2",
"type":"error_correction",
"question":"Find and correct the mistake.",
"items":[
"He don't like coffee."
],
"correct_answer":[
"He doesn't like coffee."
]
}

==================================================

12. QUALITY CONTROL CHECK

Before returning the final JSON, check every requirement:

Lesson:

✓ All content comes from the uploaded lesson.
✓ No unrelated grammar or vocabulary was added.

Vocabulary:

✓ Exactly one vocabulary activity.
✓ Exactly five gaps.
✓ Exactly five words in the word box.
✓ Every word is used once.
✓ Paragraph is realistic and contextual.
✓ Vocabulary meaning is demonstrated through context.

Grammar:

✓ Grammar matches the lesson.
✓ Enough practice items are included.
✓ Sentences are meaningful.

Reading:

✓ Complete realistic passage.
✓ Comprehension questions included.
✓ Questions require reading.

Writing:

✓ Realistic communication task.
✓ Clear marking criteria.

Answer key:

✓ Separate list.
✓ Fixed answers only.
✓ Correct IDs.

Format:

✓ Valid JSON only.
✓ No explanations outside JSON.
✓ No markdown.
✓ No extra fields.

==================================================
STRUCTURE VALIDATION RULE:

Before returning JSON, verify the structure:

Every section MUST have:

"title": "Section name",
"questions": []

The "questions" field MUST ALWAYS be an array.

Never return:

"questions": {}

Never return:

"questions": "..."

Never return a single question object without brackets.

Correct:

{
"title":"Writing",
"questions":[
{
"id":"writing_1",
"type":"writing",
"question":"Write an email..."
}
]
}

13. OUTPUT FORMAT

Return ONLY valid JSON.

Use exactly this structure:

{
"lesson_summary":"",
"title":"",
"sections":[
{
"title":"Vocabulary",
"questions":[]
},
{
"title":"Grammar",
"questions":[]
},
{
"title":"Reading",
"passage":"",
"questions":[]
},
{
"title":"Writing",
"questions":[]
},
{
"title":"Challenge",
"questions":[]
}
],
"answer_key":[]
}

Do not add:

- explanations
- comments
- markdown
- additional sections

Return JSON only.

==================================================
"""


        prompt = f"""
Create a homework worksheet in JSON format.

Lesson code:

{lesson_code}

Lesson content:

{lesson_text}

Return the homework as JSON only.
"""

        return self._json_request(
            instructions,
            prompt,
        )


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


    def mark_homework(
        self,
        homework: dict,
        student_answers: dict,
    ) -> dict:

        results = []
        writing_feedback = []


        answer_key = homework.get("answer_key", [])


        answer_lookup = {}


        for item in answer_key:

            question_id = item["id"]
            correct = item["correct_answer"]


            if isinstance(correct, dict):

                for number, answer in correct.items():

                    answer_lookup[
                        f"{question_id}_{number}"
                    ] = answer


            elif isinstance(correct, list):

                for index, answer in enumerate(correct, start=1):

                    answer_lookup[
                        f"{question_id}_{index}"
                    ] = answer


            else:

                answer_lookup[question_id] = correct



        # Find open-ended questions
        open_questions = {}


        for section in homework.get("sections", []):

            for question in section.get("questions", []):

                if question.get("type") in [
                    "writing",
                    "creative_communication",
                ]:

                    open_questions[question["id"]] = {
                        "question": question.get("question"),
                        "answer": question.get("correct_answer", "")
                    }



        for question_id, student_answer in student_answers.items():


            # AI marking for writing tasks
            if question_id in open_questions:


                feedback = self.check_open_question(
                    open_questions[question_id],
                    student_answer
                )


                writing_feedback.append({
                    "id": question_id,
                    "student_answer": student_answer,
                    "feedback": feedback
                })

                continue



            # Automatic marking for normal questions
            if question_id not in answer_lookup:
                continue


            correct_answer = answer_lookup[question_id]


            is_correct = (
                str(student_answer).strip().lower()
                ==
                str(correct_answer).strip().lower()
            )


            results.append({
                "id": question_id,
                "correct": is_correct,
                "student_answer": student_answer,
                "correct_answer": correct_answer
            }) 

            



        return {
            "results": results,
            "writing_feedback": writing_feedback
        }



    def check_writing(
        self,
        task: dict,
        student_answer: str,
    ) -> dict:


        instructions = """
You are an experienced English teacher marking student writing.

Evaluate the student's writing using the provided criteria.

Give supportive but honest feedback.

Always include at least one strength, even if the writing needs improvement.

Do not give a score.

Return JSON only:

{
 "strengths": [
   "At least one positive point about the student's writing"
 ],
 "areas_to_improve": [
   "Specific improvements"
 ],
 "teacher_comment": "A short encouraging teacher comment"
}
"""


        prompt = f"""

Writing task:

{task["question"]}


Marking criteria:

{json.dumps(task["criteria"], indent=2)}


Student answer:

{student_answer}


Analyse the writing.

Focus on:

- grammar accuracy
- vocabulary
- organisation
- task achievement
- clarity

Return JSON only.

"""


        return self._json_request(
            instructions,
            prompt
        )

    def check_open_question(
        self,
        task: dict,
        student_answer: str,
    ) -> dict:


        instructions = """
You are an experienced English teacher marking reading comprehension answers.

Your job is to check whether the student's answer shows the correct understanding of the reading text.

IMPORTANT:

Reading questions are OPEN-ENDED.

Do NOT require the exact wording of the model answer.

Accept answers that:

- have the same meaning
- use different words
- use different pronouns
- use shorter answers
- paraphrase the idea correctly

Do NOT mark an answer wrong only because the wording is different.

Example:

Model answer:
"They fell and twisted their ankle."

Student answer:
"He twisted his ankle."

Result:
Correct.

Example:

Model answer:
"She was nervous because it was her first competition."

Student answer:
"She felt worried because it was her first time."

Result:
Correct.

Only mark incorrect when the student's answer changes the meaning or gives information that is not supported by the text.

Return JSON only:

{
"correct": true,
"comment": "Short teacher comment"
}
"""


        prompt = f"""

Reading question:

{task["question"]}


Expected answer:

{task.get("answer","")}


Student answer:

{student_answer}


Decide if the student's answer has the same meaning.

Return JSON only.

"""


        return self._json_request(
            instructions,
            prompt
        )