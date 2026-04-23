# 🎓 SchoolBot — Rule-Based Academic Chatbot with Voice

A clean, beginner-friendly yet professionally structured **rule-based chatbot** for school-related queries. Built with **Python (Flask)** on the backend and **vanilla HTML/CSS/JS** on the frontend, with full **voice input & voice output** support via the Web Speech API.

---

## 📁 Project Structure

```
chatbot-project/
├── backend/
│   ├── app.py            ← Flask REST API (routes)
│   ├── chatbot.py        ← NLP engine (tokenization + intent matching)
│   ├── intents.py        ← All intents, patterns, and responses
│   └── requirements.txt  ← Python dependencies
│
├── frontend/
│   ├── index.html        ← Chat UI structure
│   ├── style.css         ← All styles (responsive, dark academic theme)
│   └── script.js         ← Chat logic + Speech Recognition + TTS
│
└── README.md             ← This file
```

---

## ⚙️ Tech Stack

| Layer     | Technology                            |
|-----------|---------------------------------------|
| Backend   | Python 3.10+ · Flask · Flask-CORS     |
| NLP       | NLTK (tokenization, stemming)         |
| Frontend  | HTML5 · CSS3 · Vanilla JavaScript     |
| Voice In  | Web Speech API (SpeechRecognition)    |
| Voice Out | Web Speech API (SpeechSynthesis / TTS)|

---

## 🚀 Setup & Run Instructions

### Prerequisites
- Python 3.10 or higher
- A modern browser (Chrome or Edge recommended for voice)
- `pip` package manager

---

### Step 1 — Clone or Download the Project

If you downloaded as a ZIP, extract it. Then open a terminal in the project root.

---

### Step 2 — Set Up the Python Backend

```bash
# Navigate to the backend folder
cd chatbot-project/backend

# (Optional but recommended) Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**NLTK resources are downloaded automatically** the first time `chatbot.py` runs.  
If you're on a restricted network, pre-download manually:

```python
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
```

---

### Step 3 — Start the Flask Server

```bash
# From inside backend/
python app.py
```

You should see:

```
=======================================================
  🎓 SchoolBot API starting...
  📡 Listening at http://127.0.0.1:5000
  POST /chat  →  { "message": "your question" }
=======================================================
```

---

### Step 4 — Open the Frontend

Open `frontend/index.html` in your browser.

> ⚠️ **Important:** Open it directly as a file (double-click) **or** serve it with a simple HTTP server.  
> Voice features (microphone) require either `localhost` or `HTTPS` in most browsers.

**Recommended — serve with Python:**

```bash
# From inside frontend/ (in a new terminal)
cd chatbot-project/frontend
python -m http.server 8080
```

Then visit: `http://localhost:8080`

---

## 🎤 Voice Features

| Feature              | How to Use                                          |
|----------------------|-----------------------------------------------------|
| **Voice Input (STT)**| Click the 🎤 microphone button, speak, auto-sends  |
| **Voice Output (TTS)**| Bot automatically reads its replies aloud          |
| **Cancel Voice**     | Click ✕ in the voice banner to cancel              |
| **Stop Typing**      | Click the stop ■ icon while the mic is active      |

> **Browser support:** Chrome and Edge work best. Firefox has partial support.  
> You will be prompted to **allow microphone access** the first time.

---

## 💬 Supported Intents (18 total)

| Intent             | Example Queries                                     |
|--------------------|-----------------------------------------------------|
| greeting           | "Hello", "Hi there", "Good morning"                |
| farewell           | "Bye", "Goodbye", "See you later"                  |
| thanks             | "Thank you", "Thanks", "Appreciate it"             |
| bot_identity       | "Who are you?", "Are you a bot?"                   |
| help               | "Help", "What can you do?", "Show me options"      |
| course_info        | "What courses are available?", "Course list"       |
| exam_schedule      | "When are exams?", "Exam timetable"                |
| assignment_deadline| "When is assignment due?", "Submission deadline"   |
| registration       | "How do I register?", "Course registration"        |
| tuition_fees       | "How much is school fees?", "Tuition payment"      |
| library            | "Library hours", "How to borrow books"             |
| hostel             | "Accommodation", "How to get a hostel room"        |
| cafeteria          | "Where to eat on campus?", "Cafeteria hours"       |
| admission          | "How to apply?", "Admission requirements"          |
| scholarship        | "How to get a scholarship?", "Financial aid"       |
| results            | "How to check results?", "My GPA"                  |
| lecturer_contact   | "How to reach my lecturer?", "Staff contacts"      |
| semester_dates     | "When does school resume?", "Academic calendar"    |

---

## 🛠️ API Reference

### `POST /chat`

**Request:**
```json
{
  "message": "When are the exams?"
}
```

**Response:**
```json
{
  "response": "📅 Exam Schedule:\n• First Semester exams are typically held in December/January...",
  "intent": "exam_schedule",
  "confidence": "matched"
}
```

---

## 🔧 Customisation

### Add a new intent
Open `backend/intents.py` and add a new dictionary to the `INTENTS` list:

```python
{
    "intent": "wifi_info",
    "patterns": ["wifi", "internet", "network", "campus wifi", "connect"],
    "responses": [
        "📶 Campus WiFi: Connect to 'UniNet' — use your matric number as password."
    ]
}
```

That's all — no retraining needed!

---

## 📋 Notes for University Submission

- This is a **rule-based** chatbot — no machine learning or external AI APIs.
- NLP pipeline: **lowercase → punctuation removal → tokenize → stopword filter → Porter stemming**.
- Intent matching uses a **weighted scoring system** across keyword patterns.
- Voice input uses the **browser-native Web Speech API** (no server-side processing).
- The project follows **separation of concerns**: routes (`app.py`), NLP logic (`chatbot.py`), knowledge base (`intents.py`), and UI (`frontend/`).

---

## 🌐 Deployment (Optional)

To make this publicly accessible:
1. Deploy Flask to **Render**, **Railway**, or **PythonAnywhere**.
2. Update `API_URL` in `script.js` to the deployed backend URL.
3. Host the frontend on **GitHub Pages**, **Netlify**, or **Vercel**.

---

*Built with ❤️ as a university project. Rule-based, clean, and fully voice-enabled.*
