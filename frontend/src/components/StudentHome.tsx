import { useState } from "react";
import { BookOpen, ArrowRight } from "lucide-react";

interface StudentHomeProps {
  onGenerate: (lessonCode: string) => void;
  loading: boolean;
  error: string;
}


export function StudentHome({
  onGenerate,
  loading,
  error,
}: StudentHomeProps) {

  const [lessonCode, setLessonCode] = useState("");


  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    onGenerate(lessonCode);
  }


  return (

    <main className="student-home">

      <section className="welcome-card">


        <div className="welcome-icon">
          <BookOpen size={40}/>
        </div>


        <h1>
          Your Personalised English Homework
        </h1>


        <p className="welcome-text">
          Personalised English homework generated from your teacher's lesson.
        </p>


        <form
          onSubmit={handleSubmit}
          className="lesson-form"
        >


          <label>
            Enter your lesson code
          </label>


          <input

            type="text"

            value={lessonCode}

            onChange={(e)=>
              setLessonCode(e.target.value)
            }

            placeholder="Example: E004CEA"

          />


          <button
            className="submit-button"
            disabled={loading}
          >

            {
              loading
              ?
              "Preparing homework..."
              :
              "Start Homework"
            }

            <ArrowRight size={20}/>

          </button>


        </form>


        {
          error &&

          <p className="error-message">
            {error}
          </p>

        }


      </section>


    </main>

  );

}