"""
intents.py
----------
Defines the rule-based intent knowledge base for the School Chatbot.
Each intent contains:
  - patterns : list of keyword/phrase triggers (lowercase)
  - responses: list of possible bot replies (one is picked at random)
"""

import random

INTENTS = [
    # ─────────────────────────────────────────────────
    # 1. GREETING
    # ─────────────────────────────────────────────────
    {
        "intent": "greeting",
        "patterns": ["hello", "hi", "hey", "good morning", "good afternoon",
                     "good evening", "howdy", "what's up", "sup", "greetings"],
        "responses": [
            "Hello! 👋 Welcome to SchoolBot. How can I help you today?",
            "Hi there! I'm SchoolBot. Ask me anything about your school.",
            "Hey! Great to see you. What would you like to know?"
        ]
    },

    # ─────────────────────────────────────────────────
    # 2. FAREWELL
    # ─────────────────────────────────────────────────
    {
        "intent": "farewell",
        "patterns": ["bye", "goodbye", "see you", "take care", "later",
                     "farewell", "quit", "exit", "ciao", "ttyl"],
        "responses": [
            "Goodbye! 👋 Have a productive day!",
            "See you later! Feel free to return if you have more questions.",
            "Take care! Good luck with your studies! 📚"
        ]
    },

    # ─────────────────────────────────────────────────
    # 3. THANKS
    # ─────────────────────────────────────────────────
    {
        "intent": "thanks",
        "patterns": ["thank you", "thanks", "thank u", "appreciate it",
                     "cheers", "much appreciated", "thx", "ty"],
        "responses": [
            "You're welcome! 😊 Is there anything else I can help with?",
            "Happy to help! Let me know if you need anything else.",
            "Anytime! 🙌 That's what I'm here for."
        ]
    },

    # ─────────────────────────────────────────────────
    # 4. BOT IDENTITY
    # ─────────────────────────────────────────────────
    {
        "intent": "bot_identity",
        "patterns": ["who are you", "what are you", "your name",
                     "are you a bot", "are you human", "what is your name",
                     "introduce yourself", "tell me about yourself"],
        "responses": [
            "I'm SchoolBot 🤖 — your rule-based academic assistant! I can help with courses, exams, schedules, and general school info.",
            "I'm SchoolBot, an AI-powered assistant designed to answer your school-related questions. Ask away!",
            "Call me SchoolBot! I'm here to make school life a little easier. 🎓"
        ]
    },

    # ─────────────────────────────────────────────────
    # 5. HELP
    # ─────────────────────────────────────────────────
    {
        "intent": "help",
        "patterns": ["help", "what can you do", "what do you know",
                     "guide me", "options", "commands", "features", "menu"],
        "responses": [
            (
                "Here's what I can help you with:\n"
                "📚 Course Information\n"
                "📅 Exam Schedules\n"
                "⏰ Assignment Deadlines\n"
                "🗓️ Semester Dates\n"
                "💰 Tuition & Fees\n"
                "📖 Library Info\n"
                "🏠 Hostel / Accommodation\n"
                "🍽️ Cafeteria\n"
                "🎓 Admission Info\n"
                "🏆 Scholarships\n"
                "📊 Results & Grades\n"
                "📞 Lecturer Contacts\n\n"
                "Just type your question naturally!"
            )
        ]
    },

    # ─────────────────────────────────────────────────
    # 6. COURSE INFORMATION
    # ─────────────────────────────────────────────────
    {
        "intent": "course_info",
        "patterns": ["course", "courses", "subject", "subjects", "module",
                     "modules", "unit", "curriculum", "programme", "program",
                     "what courses", "available courses", "list of courses"],
        "responses": [
            (
                "📚 Course Information:\n"
                "• Courses are listed on the school portal under 'Academic Programs'.\n"
                "• Each department offers both compulsory and elective units.\n"
                "• For your specific course outline, check your department's noticeboard or contact your academic adviser.\n"
                "• Course registration opens at the start of each semester."
            ),
            (
                "📚 Our programmes span Engineering, Sciences, Arts, and Social Sciences.\n"
                "Visit the school portal or your departmental office to see the full course list for your level."
            )
        ]
    },

    # ─────────────────────────────────────────────────
    # 7. EXAM SCHEDULE
    # ─────────────────────────────────────────────────
    {
        "intent": "exam_schedule",
        "patterns": ["exam", "exams", "examination", "test schedule",
                     "when is exam", "exam date", "exam timetable",
                     "exam period", "examination schedule"],
        "responses": [
            (
                "📅 Exam Schedule:\n"
                "• First Semester exams are typically held in December/January.\n"
                "• Second Semester exams run in May/June.\n"
                "• The official timetable is released 3 weeks before exams on the school portal.\n"
                "• Always check your departmental noticeboard for updates."
            ),
            (
                "📅 Examinations are usually conducted at the end of each semester.\n"
                "Check the school portal for the official timetable — it's published 3 weeks prior to the exam period."
            )
        ]
    },

    # ─────────────────────────────────────────────────
    # 8. ASSIGNMENT / DEADLINE
    # ─────────────────────────────────────────────────
    {
        "intent": "assignment_deadline",
        "patterns": ["assignment", "deadline", "due date", "submit",
                     "submission", "coursework", "project deadline",
                     "when is assignment due", "assignment due"],
        "responses": [
            (
                "⏰ Assignment Deadlines:\n"
                "• Assignment deadlines are set by individual lecturers.\n"
                "• Always check your course outline or the course portal for specific due dates.\n"
                "• Late submissions may attract penalties — submit early!"
            ),
            (
                "⏰ Deadlines vary by course and lecturer.\n"
                "Check your LMS (Learning Management System) or ask your course lecturer directly for exact due dates."
            )
        ]
    },

    # ─────────────────────────────────────────────────
    # 9. REGISTRATION
    # ─────────────────────────────────────────────────
    {
        "intent": "registration",
        "patterns": ["register", "registration", "course registration",
                     "how to register", "how do i register",
                     "register for courses", "register for course",
                     "sign up for course", "enroll",
                     "enrollment", "school registration", "portal registration"],
        "responses": [
            (
                "📝 Course Registration:\n"
                "1. Log in to the school portal with your matric number.\n"
                "2. Navigate to 'Course Registration'.\n"
                "3. Select your department and level.\n"
                "4. Add compulsory and elective courses.\n"
                "5. Confirm and print your registration slip.\n"
                "⚠️ Registration closes at the end of the third week of resumption."
            )
        ]
    },

    # ─────────────────────────────────────────────────
    # 10. TUITION & FEES
    # ─────────────────────────────────────────────────
    {
        "intent": "tuition_fees",
        "patterns": ["fee", "fees", "tuition", "school fees", "how much",
                     "payment", "pay fees", "school charges", "cost",
                     "acceptance fee", "levy"],
        "responses": [
            (
                "💰 School Fees & Tuition:\n"
                "• School fees vary by faculty and programme level.\n"
                "• Payment is made through the school's official payment portal or designated bank.\n"
                "• Fees must be cleared before course registration is approved.\n"
                "• Contact the Bursary Department for exact fee schedules."
            )
        ]
    },

    # ─────────────────────────────────────────────────
    # 11. LIBRARY
    # ─────────────────────────────────────────────────
    {
        "intent": "library",
        "patterns": ["library", "books", "borrow book", "library hours",
                     "reading room", "e-library", "digital library",
                     "library open", "library close"],
        "responses": [
            (
                "📖 Library Information:\n"
                "• Opening hours: Monday–Friday 8:00 AM – 10:00 PM\n"
                "• Saturday: 9:00 AM – 5:00 PM\n"
                "• Sunday: Closed (during exam periods, hours are extended)\n"
                "• Students can borrow up to 4 books at a time for 2 weeks.\n"
                "• The e-library is accessible 24/7 via the school portal."
            )
        ]
    },

    # ─────────────────────────────────────────────────
    # 12. HOSTEL / ACCOMMODATION
    # ─────────────────────────────────────────────────
    {
        "intent": "hostel",
        "patterns": ["hostel", "accommodation", "housing", "dorm",
                     "dormitory", "room", "stay", "living on campus",
                     "where to stay", "hall of residence"],
        "responses": [
            (
                "🏠 Hostel & Accommodation:\n"
                "• On-campus hostels are available for both male and female students.\n"
                "• Hostel allocation is done via the school portal during registration.\n"
                "• Spaces are limited — apply early!\n"
                "• Off-campus alternatives are available in nearby neighbourhoods.\n"
                "• Contact the Students' Affairs Office for more details."
            )
        ]
    },

    # ─────────────────────────────────────────────────
    # 13. CAFETERIA
    # ─────────────────────────────────────────────────
    {
        "intent": "cafeteria",
        "patterns": ["cafeteria", "canteen", "food", "eat", "restaurant",
                     "dining", "lunch", "breakfast", "dinner", "meal",
                     "food on campus"],
        "responses": [
            (
                "🍽️ Cafeteria & Dining:\n"
                "• The main cafeteria is located at the Student Centre.\n"
                "• Opening hours: 7:00 AM – 8:00 PM on weekdays.\n"
                "• Affordable meal options are available — breakfast, lunch, and dinner.\n"
                "• Several smaller food stalls are also spread across campus."
            )
        ]
    },

    # ─────────────────────────────────────────────────
    # 14. ADMISSION
    # ─────────────────────────────────────────────────
    {
        "intent": "admission",
        "patterns": ["admission", "apply", "how to apply", "application",
                     "entry requirements", "admission requirements",
                     "get admitted", "jamb", "post utme", "direct entry"],
        "responses": [
            (
                "🎓 Admission Information:\n"
                "• Applications are made through the school's official admissions portal.\n"
                "• Requirements: WAEC/NECO O'Level results + JAMB score (for UTME candidates).\n"
                "• Direct Entry candidates need an OND, NCE, or A'Level qualification.\n"
                "• Post-UTME screening is conducted after JAMB results are released.\n"
                "• Check the school website for specific cut-off marks per department."
            )
        ]
    },

    # ─────────────────────────────────────────────────
    # 15. SCHOLARSHIP
    # ─────────────────────────────────────────────────
    {
        "intent": "scholarship",
        "patterns": ["scholarship", "bursary", "award", "financial aid",
                     "grant", "sponsorship", "free tuition", "funding",
                     "student support", "financial support"],
        "responses": [
            (
                "🏆 Scholarships & Bursaries:\n"
                "• The school offers merit-based scholarships to top students.\n"
                "• State government bursaries are available for indigene students.\n"
                "• TETFUND and other federal scholarships are also accessible.\n"
                "• Visit the Students' Affairs Office or the school website for application details."
            )
        ]
    },

    # ─────────────────────────────────────────────────
    # 16. RESULTS / GRADES
    # ─────────────────────────────────────────────────
    {
        "intent": "results",
        "patterns": ["result", "results", "grade", "grades", "gpa", "cgpa",
                     "check result", "academic performance", "score",
                     "transcript", "grade point"],
        "responses": [
            (
                "📊 Results & Grades:\n"
                "• Semester results are published on the school portal after the exams.\n"
                "• Log in with your matric number to view your results.\n"
                "• GPA is calculated on a 5.0 scale.\n"
                "• For grade disputes or recomputation requests, contact your departmental exam officer."
            )
        ]
    },

    # ─────────────────────────────────────────────────
    # 17. LECTURER CONTACT
    # ─────────────────────────────────────────────────
    {
        "intent": "lecturer_contact",
        "patterns": ["lecturer", "professor", "teacher", "contact lecturer",
                     "how to reach lecturer", "lecturer office", "staff",
                     "hod", "head of department", "faculty contact"],
        "responses": [
            (
                "📞 Lecturer Contacts:\n"
                "• Lecturer details are listed on the faculty/department pages of the school website.\n"
                "• Office hours are typically posted on office doors and the school portal.\n"
                "• For urgent matters, contact the Departmental Secretary.\n"
                "• Always be respectful and professional when reaching out."
            )
        ]
    },

    # ─────────────────────────────────────────────────
    # 18. SEMESTER DATES
    # ─────────────────────────────────────────────────
    {
        "intent": "semester_dates",
        "patterns": ["semester", "academic calendar", "resumption", "vacation",
                     "school calendar", "when does school resume",
                     "when does semester start", "holiday", "break"],
        "responses": [
            (
                "🗓️ Semester & Academic Calendar:\n"
                "• First Semester: October – February\n"
                "• Second Semester: March – July\n"
                "• Long Vacation: August – September\n"
                "• The full academic calendar is available on the school portal under 'Academic Affairs'.\n"
                "• Resumption dates may vary — always check official announcements."
            )
        ]
    },
]


def get_fallback_responses():
    """Returns a list of graceful fallback responses."""
    return [
        "🤔 Hmm, I'm not sure about that. Try asking about courses, exams, fees, or hostel.",
        "Sorry, I didn't quite get that. Can you rephrase? Or type 'help' to see what I can do.",
        "I don't have information on that yet. Try asking about exams, registration, or scholarships!",
        "That's outside my knowledge base. Type 'help' to see the topics I can assist with.",
    ]


def get_response(intent_name: str) -> str:
    """Return a random response for a matched intent."""
    for intent in INTENTS:
        if intent["intent"] == intent_name:
            return random.choice(intent["responses"])
    return random.choice(get_fallback_responses())
