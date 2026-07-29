import { Send } from "lucide-react";
import type { Worksheet } from "../types";

interface WorksheetViewProps {
  worksheet: Worksheet;
  answers: Record<string, string>;
  submitting: boolean;
  onAnswer: (id: string, value: string) => void;
  onSubmit: () => void;
}

function AnswerBox({
  id,
  value,
  rows = 3,
  onAnswer,
}: {
  id: string;
  value: string;
  rows?: number;
  onAnswer: (id: string, value: string) => void;
}) {
  return (
    <textarea
      className="answer-box"
      value={value}
      onChange={(e) => onAnswer(id, e.target.value)}
      rows={rows}
      placeholder="Write your answer here..."
    />
  );
}

export function WorksheetView({
  worksheet,
  answers,
  submitting,
  onAnswer,
  onSubmit,
}: WorksheetViewProps) {


  let questionNumber = 0;



  function VocabularyGapFill({
    question,
  }: {
    question: any;
  }) {


    const words = Array.isArray(question.options)
      ? question.options
      : [];


    const text = Array.isArray(question.items)
      ? question.items[0]
      : question.items || "";


    const blanks =
      text.split(/_{3,}/).length - 1;



    let savedAnswers:string[] = [];


    try {

      savedAnswers =
        answers[question.id]
        ? JSON.parse(answers[question.id])
        : Array(blanks).fill("");

    } catch {

      savedAnswers = Array(blanks).fill("");

    }



    function updateAnswers(updated:string[]) {

      onAnswer(
        question.id,
        JSON.stringify(updated)
      );

    }



    function chooseWord(word:string) {


      const firstEmpty =
        savedAnswers.findIndex(
          (answer:string) => answer === ""
        );


      if(firstEmpty === -1){
        return;
      }



      const updated = [...savedAnswers];


      updated[firstEmpty] = word;


      updateAnswers(updated);

    }



    function removeWord(index:number) {


      const updated = [...savedAnswers];


      updated[index] = "";


      updateAnswers(updated);

    }



    function resetWords() {


      updateAnswers(
        Array(blanks).fill("")
      );

    }



    const remainingWords =
      words.filter(
        (word:string)=>
          !savedAnswers.includes(word)
      );




    function renderText() {


      const parts =
        text.split(/_{3,}/);



      return parts.map(
        (part:string,index:number)=>(


          <span key={index}>


            {part}


            {
            index < parts.length - 1 &&

            <button
              className="blank-box"
              onClick={() =>
                removeWord(index)
              }
            >

              {
              savedAnswers[index]
              ||
              "______"
              }

            </button>

            }


          </span>


        )

      );


    }



    return (

      <div className="vocabulary-gap-fill">


        <h5>
          Choose the correct words from the box:
        </h5>



        <div className="word-box">


          {
          remainingWords.map(
            (word:string)=>(


            <button
              key={word}
              className="word-card"
              onClick={() =>
                chooseWord(word)
              }
            >

              {word}

            </button>


          ))

          }


        </div>




        <div className="vocabulary-paragraph">


          <p>
            {renderText()}
          </p>


        </div>




        <button
          className="reset-button"
          onClick={resetWords}
        >

          Reset Answers

        </button>



      </div>

    );


  }

  function VocabularyMultipleChoice({
    question,
  }: {
    question: any;
  }) {

    return (

      <div className="vocabulary-multiple-choice">

        {
        Array.isArray(question.readingItems) &&
        question.readingItems.map(
          (item:any, index:number)=>(

          <div
            className="vocabulary-question"
            key={index}
          >

            <p>
              {index + 1}. {item.sentence}
            </p>


            <div className="options">

              {
              item.options.map(
                (option:string)=>(

                <label
                  className="option-card"
                  key={option}
                >

                  <input
                    type="radio"
                    name={`${question.id}_${index + 1}`}                    value={option}

                    checked={
                      answers[`${question.id}_${index + 1}`] === option
                    }

                    onChange={() =>
                      onAnswer(
                        `${question.id}_${index + 1}`,
                        option
                      )
                    }

                  />

                  <span>
                    {option}
                  </span>

                </label>

              ))

              }

            </div>

          </div>

        ))

        }

      </div>

    );

  }

  function renderQuestion(question:any) {

    questionNumber++;


    return (

      <article
        className="question-card"
        key={question.id ?? questionNumber}
      >


        <div className="question-number">
          Question {questionNumber}
        </div>



        <h4>
          {question.question}
        </h4>




        {/* Vocabulary */}

{
(question.type === "vocabulary_drag_drop" ||
question.type === "vocabulary_gap_fill") &&

<VocabularyGapFill
  question={question}
/>

}


{
question.type === "vocabulary_multiple_choice" &&

<VocabularyMultipleChoice
  question={question}
/>

}



{/* Reading */}

{
question.passage &&

<div className="reading-container">


  <div className="reading-passage">

    <h5>
      Reading text
    </h5>


    <p>
      {question.passage}
    </p>


  </div>



  {
  Array.isArray(question.readingItems) &&

  <div className="reading-questions">


    <h5>
      Write True or False for each of the following statements.
    </h5>



    {
    question.readingItems.map(
      (statement:any)=>(


      <div
        className="sub-question"
        key={statement.id}
      >


        <p>
          {statement.question}
        </p>



        <div className="options">


          <label className="option-card">


            <input
              type="radio"
              name={statement.id}
              value="True"

              checked={
                answers[
  `${question.id}_${statement.id.replace("statement_", "")}`
] === "True"
              }


              onChange={() =>
                onAnswer(
                    `${question.id}_${statement.id.replace("statement_", "")}`,
                  "True"
                )
              }

            />


            <span>
              True
            </span>


          </label>





          <label className="option-card">


            <input
              type="radio"
              name={`${question.id}_${statement.id}`}
              value="False"

              checked={
                answers[
 `${question.id}_${statement.id.replace("statement_", "")}`
] === "False"
              }


              onChange={() =>
                onAnswer(
 `${question.id}_${statement.id.replace("statement_", "")}`,
 "False"
)
              }

            />


            <span>
              False
            </span>


          </label>



        </div>


      </div>


    )

    )


    }



  </div>

  }



</div>

}

{/* Grammar and written exercises */}

{
question.type !== "vocabulary_drag_drop" &&

question.type !== "vocabulary_gap_fill" &&

question.type !== "vocabulary_multiple_choice" &&

question.type !== "true_false" &&


<div className="exercise-list">


{

Array.isArray(question.items) &&

question.items.map(
  (item:any, index:number)=>(

    <div
      className="exercise-item"
      key={index}
    >

      <span>
        {
          typeof item === "object"
          ? `${index + 1}. ${item.sentence}`
          : `${index + 1}. ${item}`
        }
      </span>


      <AnswerBox

        id={`${question.id}_${index + 1}`}

        value={
          answers[`${question.id}_${index + 1}`] ?? ""
        }

        rows={3}

        onAnswer={onAnswer}

      />


    </div>

  )

)

}



{

!Array.isArray(question.items) && question.items &&

<div className="exercise-item">

  <span>
    {question.items}
  </span>


  <AnswerBox

    id={question.id}

    value={
      answers[question.id] ?? ""
    }

    rows={7}

    onAnswer={onAnswer}

  />

</div>

}


</div>

}


        {/* Multiple choice */}


        {
        question.options &&

        question.type !== "vocabulary_drag_drop" &&

        question.type !== "vocabulary_gap_fill" &&


        <div className="options">


        {

        Array.isArray(question.options)

        ?

        question.options.map(
          (option:string)=>(


          <label
            className="option-card"
            key={option}
          >


<input
  type="radio"
  name={question.id}
  value={option}

  checked={
    answers[question.id] === option
  }


  onChange={() =>
    onAnswer(
      question.id,
      option
    )
  }

/>



            <span>
              {option}
            </span>


          </label>


        ))


        :


        Object.entries(question.options).map(
          ([key,value]:any)=>(


          <label
            className="option-card"
            key={key}
          >


            <input
              type="radio"
              name={question.id}
              value={key}


              checked={
                answers[question.id] === key
              }



              onChange={() =>
                onAnswer(
                  question.id,
                  key
                )
              }

            />



            <span>
              {key}) {value}
            </span>


          </label>


        ))

        }


        </div>

        }




        {/* Open tasks */}


        {
        !question.items &&
        !question.options &&
        !question.passage &&

        question.type !== "vocabulary_drag_drop" &&

        question.type !== "vocabulary_gap_fill" &&



        <AnswerBox
  id={question.id}
  value={answers[question.id] ?? ""}
  rows={
    question.type === "open_task" ||
    question.type === "creative_communication"
      ? 7
      : 4
  }
  onAnswer={onAnswer}
/>

        }





        {/* Writing criteria */}


        {
        Array.isArray(question.marking_criteria) &&


        <div className="criteria">


          <h5>
            Remember to include:
          </h5>



          <ul>


          {
          question.marking_criteria.map(
            (criterion:string)=>(


            <li key={criterion}>
              {criterion}
            </li>


          ))

          }


          </ul>



        </div>

        }



      </article>

    );


  }

  return (

    <section className="worksheet">


      <header className="worksheet-header">


        <p className="lesson-code">
          {worksheet.lesson_code}
        </p>



        <h1>
          {worksheet.title}
        </h1>



        {
        worksheet.lesson_summary &&

        <p className="summary">
          {worksheet.lesson_summary}
        </p>

        }


      </header>





      {
      Array.isArray(worksheet.sections) &&

      worksheet.sections.map(
        (section:any)=>(


        <section
          className="worksheet-section"
          key={section.title}
        >


          <h2>
            {section.title}
          </h2>



{
Array.isArray(section.questions)
?
section.questions.map(
  (question:any) =>
    renderQuestion({
      ...question,
      passage: section.passage,
      readingItems: question.items
    })
)
:
null
}



        </section>


      ))

      }





      <button

        className="submit-button"

        onClick={onSubmit}

        disabled={submitting}

      >


        {
        submitting
        ?
        "Checking homework..."
        :
        "Submit Homework"
        }



        <Send size={18}/>


      </button>



    </section>

  );


}
