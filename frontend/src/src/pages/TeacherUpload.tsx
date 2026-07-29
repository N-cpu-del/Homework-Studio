import { useState } from "react";
import { saveLesson } from "../../api";

export function TeacherUpload() {
  const [lessonCode, setLessonCode] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);


  async function handleUpload() {

    if (!lessonCode.trim()) {
      alert("Please enter a lesson code.");
      return;
    }


    if (!file) {
      alert("Please choose a PDF file.");
      return;
    }


    try {

      setUploading(true);


      const result = await saveLesson(
        lessonCode,
        file
      );


      alert(
        `Lesson uploaded successfully: ${result.lesson_code}`
      );


      setLessonCode("");
      setFile(null);


    } catch (error:any) {

      alert(
        error.message || "Upload failed."
      );

    } finally {

      setUploading(false);

    }

  }



  return (

    <main className="worksheet">


      <section className="worksheet-header">

        <h1>
          Teacher Upload
        </h1>


        <p className="summary">
          Upload a lesson PDF. Students can use the lesson code to generate homework.
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
            placeholder="Example: ARS_B1_05"
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

          disabled={uploading}

        >

          {
            uploading
            ? "Uploading..."
            : "Upload Lesson"
          }


        </button>




      </section>


    </main>

  );

}