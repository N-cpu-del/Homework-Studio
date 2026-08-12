import { Send } from "lucide-react";
import type { Question, Worksheet, WorksheetItem } from "../types";

interface WorksheetViewProps {
  worksheet: Worksheet;
  answers: Record<string, string>;
  submitting: boolean;
  onAnswer: (id: string, value: string) => void;
  onSubmit: () => void;
}

const text = (value: unknown): string =>
  typeof value === "string" ? value : typeof value === "number" || typeof value === "boolean" ? String(value) : "";

function itemText(item: WorksheetItem): string {
  return text(item.statement ?? item.sentence ?? item.question ?? item.text ?? item.prompt ?? item.content);
}

function Dialogue({ dialogue }: { dialogue: WorksheetItem["dialogue"] }) {
  if (Array.isArray(dialogue)) {
    return <>{dialogue.map((line, index) => <p key={`dialogue-${index}`} className="dialogue-line">{line.speaker ? `${line.speaker}: ` : ""}{line.text}</p>)}</>;
  }
  return dialogue ? <p style={{ whiteSpace: "pre-line" }}>{dialogue}</p> : null;
}

function AnswerBox({ id, value, onAnswer }: { id: string; value: string; onAnswer: (id: string, value: string) => void }) {
  return <textarea className="answer-box" value={value} onChange={(event) => onAnswer(id, event.target.value)} rows={7} placeholder="Write your answer here..." />;
}

function ChoiceItem({ item, number, answers, onAnswer }: { item: WorksheetItem; number: number; answers: Record<string, string>; onAnswer: (id: string, value: string) => void }) {
  const id = text(item.id).trim();
  const options = Array.isArray(item.options) ? item.options.map(text).filter(Boolean) : [];
  if (!id) {
    if (import.meta.env.DEV) console.warn("Skipping answerable item with no canonical ID", item);
    return <div className="exercise-item"><p>{itemText(item) || "This question is missing its identifier."}</p></div>;
  }
  return <div className="exercise-item" key={id}>
    <div className="question-number">Question {number}</div>
    <Dialogue dialogue={item.dialogue} />
    {itemText(item) && <p style={{ whiteSpace: "pre-line" }}>{itemText(item)}</p>}
    {options.length > 0 ? <div className="options">{options.map((option, optionIndex) => <label className="option-card" key={`${id}-option-${optionIndex}`}>
      <input type="radio" name={id} value={option} checked={answers[id] === option} onChange={() => onAnswer(id, option)} />
      <span>{option}</span>
    </label>)}</div> : <p className="missing-question">No options were provided for this question.</p>}
  </div>;
}

function OpenQuestion({ question, number, answers, onAnswer }: { question: Question; number: number; answers: Record<string, string>; onAnswer: (id: string, value: string) => void }) {
  const id = text(question.id).trim();
  if (!id) return null;
  return <article className="question-card" key={id}>
    <div className="question-number">Question {number}</div>
    {question.question && <h4>{question.question}</h4>}
    <AnswerBox id={id} value={answers[id] ?? ""} onAnswer={onAnswer} />
    {Array.isArray(question.marking_criteria) && question.marking_criteria.length > 0 && <div className="criteria"><h5>Remember to include:</h5><ul>{question.marking_criteria.map((criterion, index) => <li key={`${id}-criterion-${index}`}>{criterion}</li>)}</ul></div>}
  </article>;
}

export function WorksheetView({ worksheet, answers, submitting, onAnswer, onSubmit }: WorksheetViewProps) {
  let visualNumber = 0;
  const sections = Array.isArray(worksheet.sections) ? worksheet.sections : [];

  return <section className="worksheet">
    <header className="worksheet-header"><div className="lesson-code">{text(worksheet.lesson_code)}</div><h1>{text(worksheet.title)}</h1>{worksheet.lesson_summary && <p className="summary">{worksheet.lesson_summary}</p>}</header>
    {sections.map((section, sectionIndex) => {
      const title = text(section?.title) || "Section";
      const normalizedTitle = title.toLowerCase();
      const questions = Array.isArray(section?.questions) ? section.questions : [];
      return <section className="worksheet-section" key={`section-${sectionIndex}-${title}`}>
        <h2>{title}</h2>
        {normalizedTitle === "reading" && section.passage && <div className="reading-passage"><h5>Reading text</h5><p style={{ whiteSpace: "pre-line" }}>{section.passage}</p></div>}
        {questions.length === 0 ? <p>No questions were provided.</p> : questions.map((question, questionIndex) => {
          if (!question || typeof question !== "object") return null;
          const items = Array.isArray(question.items) ? question.items : [];
          const isOpen = normalizedTitle === "writing" || normalizedTitle === "challenge" || question.type === "writing" || question.type === "challenge" || question.type === "creative_communication";
          if (isOpen) return <OpenQuestion key={`open-${sectionIndex}-${questionIndex}-${question.id}`} question={question} number={++visualNumber} answers={answers} onAnswer={onAnswer} />;
          return <article className="question-card" key={`group-${sectionIndex}-${questionIndex}-${question.id}`}>
            {question.question && <h4>{question.question}</h4>}
            {items.length > 0 ? items.map((item, itemIndex) => <ChoiceItem key={text(item.id) || `missing-${questionIndex}-${itemIndex}`} item={item} number={++visualNumber} answers={answers} onAnswer={onAnswer} />) : <p>No answerable items were provided.</p>}
          </article>;
        })}
      </section>;
    })}
    <button type="button" className="submit-button" onClick={onSubmit} disabled={submitting}>{submitting ? "Checking homework..." : "Submit Homework"}<Send size={18} /></button>
  </section>;
}
