# MIRA - Medical Intelligence Robotic Automation

A Health Prediction Web Application that collects patient blood test data and uses AI to predict possible health conditions.

## Tech Stack
- **Frontend:** React.js
- **Backend:** Python + Flask
- **Database:** SQLite
- **AI:** Groq API (LLaMA 3.1)

## Features
- Add, View, Edit, Delete patient records (CRUD)
- AI-generated health predictions based on blood test values
- Input validation on all fields
- Persistent storage with SQLite

## How to Run

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Fields Collected
- Full Name, Date of Birth, Email
- Glucose, Haemoglobin, Cholesterol
- AI Remarks (auto-generated)

## Note
Create a `.env` file in the backend folder:
```
GROQ_API_KEY=your_key_here
```
