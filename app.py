"""
Koko Iminabo — Portfolio site backend.

Run locally with:
    pip install flask
    python app.py

Then open http://127.0.0.1:5000 in your browser.
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# Simple file-based "storage" for contact messages (no database needed).
MESSAGES_FILE = os.path.join(os.path.dirname(__file__), "messages.json")


def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_message(entry):
    messages = load_messages()
    messages.append(entry)
    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2)


# ---- Content: edit these dictionaries to update the site's data ----

PROFILE = {
    "name": "Koko Iminabo",
    "full_name": "Tamunoiminabo Adokiye \"Koko\" Iminabo",
    "tagline": "I used to parse sentences. Now I parse data.",
    "location": "Port Harcourt, Nigeria",
    "summary": (
        "I trained as a linguist, mapping the hidden structure underneath language — "
        "PRO, traces, the invisible scaffolding that makes a sentence mean something. "
        "These days I point that same instinct at data: I look for the structure "
        "underneath a spreadsheet, and turn it into something that means something."
    ),
}

SKILLS = [
    {"name": "Python", "note": "pandas, tkinter, automation scripts"},
    {"name": "SQL", "note": "querying, joins, aggregation"},
    {"name": "R", "note": "statistical analysis"},
    {"name": "Machine Learning", "note": "foundational models & evaluation"},
    {"name": "Data Visualization", "note": "clear, honest charts"},
    {"name": "Excel", "note": "modeling & reporting"},
    {"name": "Git", "note": "version control"},
    {"name": "Flask", "note": "lightweight web apps"},
]

EXPERIENCE = [
    {
        "org": "J.P. Morgan",
        "role": "Virtual Internship — Data & Analysis",
        "period": "Completed",
        "description": "Simulated real analyst tasks: working with financial data, "
                       "identifying patterns, and communicating findings clearly.",
    },
    {
        "org": "Tata Consultancy Services",
        "role": "Virtual Internship",
        "period": "Completed",
        "description": "Practiced structured problem-solving and IT-services "
                       "workflows in a simulated enterprise environment.",
    },
    {
        "org": "Quantium",
        "role": "Virtual Internship — Data Analytics",
        "period": "Completed",
        "description": "Worked through retail analytics tasks: category analysis, "
                       "customer segmentation, and translating data into a "
                       "commercial recommendation.",
    },
]

PROJECTS = [
    {
        "title": "Aduke Market",
        "tag": "Full-stack web app",
        "description": "A full-stack e-commerce prototype built with Flask, SQLite, "
                        "and vanilla HTML/CSS/JS, with a Paystack payment stub "
                        "wired for Nigerian naira transactions.",
        "stack": ["Flask", "SQLite", "JavaScript", "Paystack API"],
        "link": "#",
    },
    {
        "title": "Desktop Calculator",
        "tag": "Python / GUI",
        "description": "A calculator app built with Python's tkinter, focused on "
                        "clean event handling and a straightforward interface.",
        "stack": ["Python", "Tkinter"],
        "link": "#",
    },
    {
        "title": "Empty Categories in Syntactic Configuration",
        "tag": "MA Thesis — Linguistics",
        "description": "A cross-linguistic study of PRO, pro, NP-trace and wh-trace "
                        "using Government & Binding Theory and the Minimalist "
                        "Program, with data spanning English, Arabic, Mandarin, "
                        "Yoruba, Igbo, Hausa and Izon.",
        "stack": ["Research", "Syntax", "Cross-linguistic analysis"],
        "link": "#",
    },
]

EDUCATION = [
    {
        "credential": "B.A. English and Literary Studies",
        "school": "Niger Delta University",
    },
    {
        "credential": "HSE Diploma",
        "school": "Niger Delta University",
    },
    {
        "credential": "Data Analytics, SQL, Python, R & Machine Learning Certifications",
        "school": "Simplilearn",
    },
]

SOCIALS = {
    "email": "your-email@example.com",
    "linkedin": "https://linkedin.com/in/your-profile",
    "github": "https://github.com/your-username",
}


@app.route("/")
def home():
    return render_template(
        "index.html",
        profile=PROFILE,
        skills=SKILLS,
        experience=EXPERIENCE,
        projects=PROJECTS,
        education=EDUCATION,
        socials=SOCIALS,
        year=datetime.now().year,
    )


@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True) or request.form

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify({"ok": False, "error": "Please fill in every field."}), 400

    entry = {
        "name": name,
        "email": email,
        "message": message,
        "received_at": datetime.now().isoformat(timespec="seconds"),
    }
    save_message(entry)

    return jsonify({"ok": True, "message": "Thanks — your message has been received."})


if __name__ == "__main__":
    app.run(debug=True)
