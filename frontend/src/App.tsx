import { useState } from "react";

import { generateHomework, markHomework } from "./api";
import { FeedbackView } from "./components/FeedbackView";
import { StudentHome } from "./components/StudentHome";
import { TeacherUpload } from "./components/TeacherUpload";
import { WorksheetView } from "./components/WorksheetView";
import type { MarkingResult, Worksheet } from "./types";


export default function App() {

  const path = window.location.pathname;


  const [worksheet, setWorksheet] = useState<Worksheet | null>(null);

  const [answers, setAnswers] = useState<Record<string, string>>({});

  const [feedback, setFeedback] = useState<MarkingResult | null>(null);

  const [loading, setLoading] = useState(false);

  const [submitting, setSubmitting] = useState(false);

  const [error, setError] = useState("");



  // Teacher page
  if (path === "/teacher") {

    return <TeacherUpload />;

  }



  async function handleGenerate(lessonCode: string) {

    setError("");

    setFeedback(null);


    if (!lessonCode.trim()) {

      setError("Please enter a lesson code.");

      return;

    }


    setLoading(true);


    try {

      const generated = await generateHomework(
        lessonCode.trim()
      );


      setWorksheet(generated);

      setAnswers({});


    } catch (err) {


      setError(
        err instanceof Error
          ? err.message
          : "Unable to load this lesson."
      );


      setWorksheet(null);


    } finally {

      setLoading(false);

    }

  }




  async function handleSubmit() {


    if (!worksheet) return;


    setSubmitting(true);

    setError("");



    try {


      console.log(
        "WORKSHEET:",
        JSON.stringify(worksheet, null, 2)
      );



      const result = await markHomework(

        worksheet.lesson_code,

        worksheet,

        answers

      );



      console.log(
        "RESULT BEFORE FEEDBACK:",
        result
      );



      setFeedback(result);



    } catch (err) {



      setError(

        err instanceof Error

          ? err.message

          : "Unable to submit homework."

      );



    } finally {


      setSubmitting(false);


    }


  }





  // Student page

  if (path === "/" || path === "/student") {


    return (


      <main className="app-container">



        {!worksheet && (


          <StudentHome

            onGenerate={handleGenerate}

            loading={loading}

            error={error}

          />


        )}






        {worksheet && (


          <div className="student-work">



            <WorksheetView


              worksheet={worksheet}


              answers={answers}


              submitting={submitting}



              onAnswer={

                (questionId, value) =>

                  setAnswers(

                    (current) => ({

                      ...current,

                      [questionId]: value

                    })

                  )

              }



              onSubmit={handleSubmit}


            />






            {error && (


              <p className="error center">

                {error}

              </p>


            )}







            {feedback && (


              <FeedbackView


                worksheet={worksheet}


                result={feedback}


              />


            )}






          </div>


        )}






      </main>


    );


  }



  return null;


}