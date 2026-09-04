# AI Placement Preparation Platform

A full-stack AI-powered placement preparation platform for engineering students.

## Features

- **AI Chatbot** — Conversational AI for placement prep (DSA, HR, system design)
- **Resume Analyzer** — ATS scoring, JD matching, AI improvement suggestions
- **Personalized Roadmap** — 12-week preparation roadmap tailored to your goals
- **AI Mock Interview** — HR/Technical/Behavioral/Company-specific with scoring
- **Coding Platform** — LeetCode-style with Monaco editor and code execution
- **Aptitude Training** — Quantitative, Logical, Verbal practice
- **Company Preparation** — 10+ companies with recruitment details
- **Gamification** — XP, levels, streaks, badges

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python · FastAPI · Beanie ODM |
| Database | MongoDB (Motor async driver) |
| AI | OpenAI GPT-4o-mini (mock fallback) |
| Frontend | React 18 · Vite · Tailwind CSS |
| Editor | Monaco Editor |
| Charts | Recharts |

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB running locally

### Backend Setup

```bash
cd server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp ../.env.example ../.env
# Edit .env with your settings

# Seed the database (optional but recommended)
cd seeds
python run_seed.py

# Start the server
cd ..
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd client
cp .env.example .env
npm install
npm run dev
```

### Access

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGODB_URI` | `mongodb://localhost:27017` | MongoDB connection string |
| `JWT_SECRET` | — | Secret key for JWT signing |
| `AI_PROVIDER` | `mock` | `mock`, `openai`, or `gemini` |
| `OPENAI_API_KEY` | — | OpenAI API key (if using openai provider) |
| `CLIENT_URL` | `http://localhost:5173` | Frontend URL for CORS |

## API Endpoints

| Module | Base Path |
|--------|-----------|
| Auth | `/api/auth` |
| Chat | `/api/chat` |
| Resume | `/api/resumes` |
| Roadmap | `/api/roadmaps` |
| Interview | `/api/interviews` |
| Coding | `/api/coding` |
| Aptitude | `/api/aptitude` |
| Companies | `/api/companies` |
| Progress | `/api/progress` |

## Mock Mode

Set `AI_PROVIDER=mock` (default) to run without any API keys. The platform is fully functional with comprehensive mock responses for all AI features.

## Project Structure

```
Prompt/
├── server/                 # FastAPI backend
│   ├── app/
│   │   ├── config/         # Settings (pydantic-settings)
│   │   ├── db/             # MongoDB initialization
│   │   ├── middleware/      # JWT auth
│   │   ├── models/         # Beanie ODM models
│   │   ├── routers/        # API route handlers
│   │   ├── services/ai/    # AI service abstraction
│   │   └── utils/          # File parsers, helpers
│   ├── seeds/              # Database seed data
│   ├── main.py             # FastAPI app entry point
│   └── requirements.txt
├── client/                 # React frontend
│   ├── src/
│   │   ├── context/        # AuthContext
│   │   ├── hooks/          # useToast
│   │   ├── pages/          # All page components
│   │   ├── services/       # API service layer
│   │   └── utils/          # Helpers, constants
│   ├── package.json
│   └── vite.config.js
└── .env.example
```
