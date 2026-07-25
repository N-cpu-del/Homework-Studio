import type { MarkingResult, Worksheet } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8001";


async function parseResponse<T>(response: Response): Promise<T> {

  if (response.ok) {
    return response.json() as Promise<T>;
  }

  const body = await response.json().catch(() => ({}));

  throw new Error(body.detail ?? "Something went wrong.");

}



export async function saveLesson(
  lessonCode: string,
  file: File
): Promise<{ lesson_code: string; filename: string }> {

  const form = new FormData();

  form.append("lesson_code", lessonCode);

  form.append("pdf", file);


  const response = await fetch(
    `${API_BASE}/api/teacher/lessons`,
    {
      method: "POST",
      body: form,
    }
  );


  return parseResponse(response);

}




export async function generateHomework(
  lessonCode: string
): Promise<Worksheet> {


  const response = await fetch(
    `${API_BASE}/api/homework/generate`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        lesson_code: lessonCode,
      }),
    }
  );


  return parseResponse(response);

}





export async function markHomework(
  lessonCode: string,
  worksheet: Worksheet,
  answers: Record<string, string>,
): Promise<MarkingResult> {

  console.log("LESSON CODE SENT:", lessonCode);
  console.log("SUBMITTING HOMEWORK", answers);

  const response = await fetch(`${API_BASE}/api/homework/submit?lesson_code=${lessonCode}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(answers),
  });

  const data = await parseResponse<any>(response);

  return data.result;
}