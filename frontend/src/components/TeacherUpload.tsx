import { CheckCircle2, UploadCloud } from "lucide-react";
import { FormEvent, useState } from "react";

import { saveLesson, generateHomework } from "../api";


export function TeacherUpload() {


  const [lessonCode, setLessonCode] = useState("");

  const [file, setFile] = useState<File | null>(null);

  const [status, setStatus] = useState<string>("");

  const [error, setError] = useState<string>("");

  const [saving, setSaving] = useState(false);



  async function submit(event: FormEvent) {

    event.preventDefault();


    setError("");

    setStatus("");



    if (!lessonCode.trim() || !file) {

      setError(
        "Add a lesson code and PDF."
      );

      return;

    }



    setSaving(true);



    try {


      const saved = await saveLesson(
        lessonCode,
        file
      );



      setStatus(
        `${saved.lesson_code} uploaded. Generating homework...`
      );



      await generateHomework(
        lessonCode
      );



      setStatus(
        `${saved.lesson_code} uploaded and homework generated successfully.`
      );



    } catch (err) {


      setError(
        err instanceof Error
          ? err.message
          : "Sorry. This lesson could not be processed. Please try again later."
      );


    } finally {


      setSaving(false);


    }

  }





  return (

    <section
      className="panel teacher-panel"
      aria-labelledby="teacher-heading"
    >


      <div>

        <p className="eyebrow">
          Teacher
        </p>


        <h2 id="teacher-heading">
          Upload lesson PDF
        </h2>


      </div>




      <form
        onSubmit={submit}
        className="form-stack"
      >



        <label>

          <span>
            Lesson Code
          </span>


          <input

            value={lessonCode}

            onChange={(event) =>
              setLessonCode(
                event.target.value
              )
            }

            placeholder="G8-U5-S3"

          />


        </label>





        <label className="file-input">


          <span>
            PDF Upload
          </span>



          <input

            accept="application/pdf"

            type="file"

            onChange={(event) =>
              setFile(
                event.target.files?.[0] ?? null
              )
            }

          />



          <div className="file-box">

            <UploadCloud
              size={20}
              aria-hidden="true"
            />


            <strong>
              {file ? file.name : "Choose PDF"}
            </strong>


          </div>



        </label>





        <button

          type="submit"

          className="button secondary"

          disabled={saving}

        >

          {
            saving
              ? "Processing..."
              : "Save & Generate Homework"
          }


        </button>



      </form>





      {status && (

        <p className="success">

          <CheckCircle2
            size={16}
            aria-hidden="true"
          />

          {status}

        </p>

      )}




      {error && (

        <p className="error">
          {error}
        </p>

      )}



    </section>

  );

}