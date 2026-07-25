export type SectionName =
  | "Vocabulary"
  | "Grammar"
  | "Reading"
  | "Writing"
  | "Challenge";


export interface Question {
  id: string;
  type: string;
  question?: string;

  items?: any[];

  options?: any;

  passage?: string;

  questions?: {
    id?: string;
    type?: string;
    question?: string;

    items?: {
      id: string;
      question: string;
      correct_answer?: string;
    }[];

  }[];

  marking_criteria?: string[];
}


export interface WorksheetSection {
  title: SectionName;
  questions: Question[];
}


export interface Worksheet {
  title: string;
  lesson_code: string;
  lesson_summary?: string;

  sections: WorksheetSection[];

  answer_key?: unknown[];
}


export interface CorrectAnswer {
  question: string;
  answer: string;
}


export interface WrongAnswer {
  question: string;
  student_answer: string;
  correct_answer: string;
  explanation: string;
}


export interface MarkingResult {
  correct_answers: CorrectAnswer[];

  wrong_answers: WrongAnswer[];

  suggestions: string[];
}