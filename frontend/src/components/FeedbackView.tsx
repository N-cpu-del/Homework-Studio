import type { MarkingResult, Worksheet } from "../types";

interface FeedbackViewProps {
  worksheet: Worksheet;
  result: MarkingResult;
}


function formatQuestionName(id: string) {

  if (id.startsWith("vocab")) {

    const number = id.split("_").pop();

    return `Vocabulary - Question ${number}`;

  }


  if (id.startsWith("grammar")) {

    const number = id.split("_").pop();

    return `Grammar - Question ${number}`;

  }


  if (id.startsWith("reading")) {

    const number = id.split("_").pop();

    return `Reading - Question ${number}`;

  }


  return id;

}



export function FeedbackView({ result }: FeedbackViewProps) {


  const vocabulary = (result.results ?? [])
    .filter((item: any) => item.id.startsWith("vocab"));


  const grammar = (result.results ?? [])
    .filter((item: any) => item.id.startsWith("grammar"));


  const reading = (result.results ?? [])
    .filter((item: any) => item.id.startsWith("reading"));



  function renderSection(
    title: string,
    questions: any[]
  ) {

    if (questions.length === 0) {
      return null;
    }


    return (

      <div className="feedback-block">

        <h3>{title}</h3>


        <ul>

          {questions.map(
            (item: any, index: number) => (

            <li key={index}>


              <p>
                <strong>
                  {formatQuestionName(item.id)}
                </strong>
              </p>


              {item.correct ? (

                <p>
                  ✅ Correct
                </p>

              ) : (

                <>

                  <p>
                    ❌ Your answer: {item.student_answer}
                  </p>


                  <p>
                    Correct answer: {item.correct_answer}
                  </p>

                </>

              )}


            </li>

          ))}

        </ul>


      </div>

    );

  }



  return (

    <section className="feedback">


      <h2>
        Homework Feedback
      </h2>



      {renderSection(
        "Vocabulary",
        vocabulary
      )}



      {renderSection(
        "Grammar",
        grammar
      )}



      {renderSection(
        "Reading",
        reading
      )}



      {(result.writing_feedback ?? []).length > 0 && (

        <div className="feedback-block">

          <h3>
            Writing Feedback ✍️
          </h3>



          {(result.writing_feedback ?? []).map(
            (item: any, index: number) => (

            <div key={index}>


              <h4>
                Task {index + 1}
              </h4>


              <p>
                <strong>Your answer:</strong>
              </p>

              <p>
                {item.student_answer}
              </p>



              <h4>
                Strengths ✅
              </h4>

              <ul>

                {item.feedback?.strengths?.map(
                  (strength: string, i: number) => (

                  <li key={i}>
                    {strength}
                  </li>

                ))}

              </ul>



              <h4>
                Areas to improve ❌
              </h4>

              <ul>

                {item.feedback?.areas_to_improve?.map(
                  (area: string, i: number) => (

                  <li key={i}>
                    {area}
                  </li>

                ))}

              </ul>



              <h4>
                Teacher comment 💬
              </h4>

              <p>
                {item.feedback?.teacher_comment}
              </p>


            </div>

          ))}

        </div>

      )}



    </section>

  );

}