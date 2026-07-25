# AI Homework Assistant

A minimal web app for English teachers to upload a lesson PDF and for students to generate and submit AI-marked homework from that lesson only.

## Stack

- Frontend: React + TypeScript + Vite
- Backend: Python + FastAPI
- Database: SQLite
- PDF text extraction: PyMuPDF
- AI: OpenAI Responses API

## Quick Start

### Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Add your OpenAI API key to `backend/.env`, then run:

```powershell
uvicorn app.main:app --reload --port 8000
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal. The frontend expects the backend at `http://localhost:8000` by default.

## Notes

- Students never upload files and cannot access lesson PDFs directly.
- Blank student answers are ignored during marking.
- The default model is configurable with `OPENAI_MODEL`, currently set to `gpt-5.6-luna` in the example environment.
