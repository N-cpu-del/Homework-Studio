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

  readingItems?: any[];

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



export interface FeedbackItem {

  id: string;

  correct: boolean;

  student_answer?: string;

  correct_answer?: string;

}



export interface WritingFeedback {

  student_answer: string;

  feedback?: {

    strengths?: string[];

    areas_to_improve?: string[];

    teacher_comment?: string;

  };

}



export interface MarkingResult {

  results: FeedbackItem[];

  writing_feedback?: WritingFeedback[];

}