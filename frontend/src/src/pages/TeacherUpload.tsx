import { useState } from "react";

export function TeacherUpload() {

  const [lessonCode, setLessonCode] = useState("");

  const [file, setFile] = useState<File | null>(null);



  function handleUpload() {

    if (!lessonCode.trim()) {

      alert("Please enter a lesson code.");

      return;

    }


    if (!file) {

      alert("Please choose a PDF file.");

      return;

    }


    console.log("Lesson code:", lessonCode);

    console.log("File:", file);


    alert("Ready to upload!");

  }



  return (

    <main className="worksheet">


      <section className="worksheet-header">


        <h1>
          Teacher Upload
        </h1>


        <p className="summary">
          Upload a lesson PDF and generate homework.
        </p>


      </section>





      <section className="worksheet-section">



        <div className="exercise-item">


          <label>
            Lesson code
          </label>



          <input

            className="answer-box"

            value={lessonCode}

            onChange={(e) =>
              setLessonCode(e.target.value)
            }

            placeholder="Example: G8-U5-S3"

          />


        </div>





        <div className="exercise-item">


          <label>
            Upload lesson PDF
          </label>



          <input

            type="file"

            accept="application/pdf"

            onChange={(e) =>
              setFile(
                e.target.files?.[0] ?? null
              )
            }

          />


        </div>





        <button

          className="submit-button"

          onClick={handleUpload}

        >

          Generate Homework

        </button>




      </section>



    </main>

  );

}