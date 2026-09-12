# SIH26092 – Run Guide

## 1. Backend

Open Git Bash in `backend/`:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Health check: http://127.0.0.1:8000/health

## 2. Frontend

Open a second Git Bash in `frontend/`:

```bash
npm install
npm run dev
```

Open the Vite URL shown in the terminal, normally http://localhost:5173

## User flow

Home → Profile → Results → Scheme Details → Partners → Partner Details

The Profile page collects personal details, location, category, income, purpose and requested support amount in one place. The Results page shows both eligible schemes and clear reasons for schemes that are not eligible.
