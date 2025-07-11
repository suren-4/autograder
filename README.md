# 🧠 AutoGrader – Intelligent Answer Evaluation System

AutoGrader is an AI-powered web application that automates the grading of subjective answers. Designed for educators and institutions, it provides fast, consistent, and insightful feedback using NLP, machine learning, and LLMs.

---

## 🚀 Features

- 📝 **Multi-question Test Interface** – Students can submit answers via a sleek UI
- 🧮 **Automated Scoring** – Evaluate answers instantly with rule-based or LLM-assisted logic
- 🧾 **Detailed Feedback** – Identify errors, suggest improvements, and explain correct answers
- 📊 **CSV Batch Grading** – Upload answer sheets in bulk and get back structured grading reports
- 💬 **LLM Integration** – Uses GPT-style models to provide human-like feedback (Level 3+)
- 🌐 **Hosted UI (Level 4)** – Fully deployed demo using Streamlit or HuggingFace Spaces
- 🧠 **Advanced Add-ons (Level 5)** – Grammar check, rubric-based grading, MCQ generation (in progress)

---

## 📁 Tech Stack

| Layer         | Technology                      |
|--------------|----------------------------------|
| Frontend      | Streamlit / React (optional UI) |
| Backend       | Python, FastAPI (optional)      |
| ML/NLP        | LLMs (GPT, OpenAI), spaCy       |
| Data Storage  | CSV, Pandas                     |
| Hosting       | HuggingFace Spaces / Streamlit Cloud |

---

## ⚙️ How to Run

```bash
# 1. Clone the repo
git clone https://github.com/your-username/auto-grader.git
cd auto-grader

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
