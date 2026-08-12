export interface DialogueLine { speaker?: string; text: string; }

export interface WorksheetItem {
  id: string;
  dialogue?: DialogueLine[] | string;
  statement?: string;
  sentence?: string;
  question?: string;
  text?: string;
  prompt?: string;
  content?: string;
  options?: unknown[];
  correct_answer?: string;
}

export interface Question {
  id: string;
  type: string;
  question?: string;
  items?: WorksheetItem[];
  marking_criteria?: string[];
}

export interface WorksheetSection { title: string; passage?: string; questions?: Question[]; }
export interface Worksheet { title: string; lesson_code: string; lesson_summary?: string; sections: WorksheetSection[]; answer_key?: Array<{ id: string; correct_answer: string }>; }
export interface FeedbackItem { id: string; correct: boolean; student_answer?: string; correct_answer?: string; }
export interface WritingFeedback { id: string; student_answer: string; feedback?: { strengths?: string[]; areas_to_improve?: string[]; teacher_comment?: string; }; }
export interface MarkingResult { results: FeedbackItem[]; writing_feedback?: WritingFeedback[]; }
