import streamlit as st
import pandas as pd
import requests
import os

# Set page config with a more professional look
st.set_page_config(
    page_title="AutoGrader AI",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced styling with modern design
st.markdown("""
    <style>
        /* Main container styling */
        .main {
            background: #181a1b;
            padding: 2rem;
        }
        
        /* Title styling */
        h1 {
            color: #90caf9;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 800;
            font-size: 2.5rem;
            text-shadow: none;
            animation: fadeIn 1s ease-in;
        }
        
        /* Subtitle styling */
        .stMarkdown p {
            color: #f5f5f5;
            font-size: 1.1rem;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        /* Button styling */
        .stButton>button {
            color: #fff;
            background: #1976d2;
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            border: none;
            box-shadow: 0 4px 6px rgba(0,0,0,0.18);
            width: 100%;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.22);
            background: #1565c0;
        }
        
        /* File uploader styling */
        .stFileUploader {
            background-color: #23272a;
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.18);
            border: 1px solid #333;
            color: #f5f5f5;
        }
        
        /* DataFrame styling */
        .stDataFrame {
            background-color: #23272a;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.18);
            padding: 1rem;
            margin: 1rem 0;
            color: #f5f5f5;
        }
        
        /* Success message styling */
        .stSuccess {
            background: #264d36;
            color: #b9f6ca;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            border: none;
            box-shadow: 0 4px 6px rgba(0,0,0,0.18);
        }
        
        /* Spinner styling */
        .stSpinner {
            color: #90caf9;
        }
        
        /* Markdown text styling */
        .stMarkdown {
            color: #f5f5f5;
            line-height: 1.8;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }
        ::-webkit-scrollbar-track {
            background: #23272a;
            border-radius: 5px;
        }
        ::-webkit-scrollbar-thumb {
            background: #1976d2;
            border-radius: 5px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #1565c0;
        }
        
        /* Animation keyframes */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Card styling for results */
        .element-container {
            background-color: #23272a;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.18);
            transition: transform 0.3s ease;
            color: #f5f5f5;
        }
        .element-container:hover {
            transform: translateY(-5px);
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: #23272a;
            padding: 2rem 1rem;
            color: #90caf9 !important;
        }
        /* Sidebar text color fix */
        .css-1d391kg h2, .css-1d391kg p, .css-1d391kg li, .css-1d391kg div {
            color: #90caf9 !important;
        }
        
        /* Input field styling */
        .stTextInput>div>div>input {
            border-radius: 12px;
            border: 2px solid #333;
            padding: 0.75rem;
            transition: all 0.3s ease;
            color: #f5f5f5;
            background: #23272a;
        }
        .stTextInput>div>div>input:focus {
            border-color: #1976d2;
            box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.25);
        }
    </style>
""", unsafe_allow_html=True)

# Add a sidebar for additional information
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; color: white;'>
            <h2>📚 AutoGrader AI</h2>
            <p>Your AI-powered grading assistant</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### How to Use")
    st.markdown("""
        1. Prepare your CSV file with student answers
        2. Upload the file using the uploader
        3. Wait for AI grading
        4. Download results
    """)
    
    st.markdown("---")
    st.markdown("### Features")
    st.markdown("""
        - AI-powered grading
        - Detailed feedback
        - Similarity scoring
        - Batch processing
    """)

# --- Setup ---
LLAMA_API_KEY = "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"
LLAMA_API_URL = "https://openrouter.ai/api/v1/chat/completions"
LLAMA_MODEL = "meta-llama/llama-3-8b-instruct"  # You can also try llama-2-13b-chat or others

# Model answers
questions = [
    {"question": "What is Machine Learning?", "model_answer": "Machine Learning is a subset of AI where machines learn from data."},
    {"question": "Define supervised learning.", "model_answer": "Supervised learning is where a model learns from labeled data."},
    {"question": "What is overfitting?", "model_answer": "Overfitting is when a model learns the noise in training data, leading to poor performance on new data."},
    {"question": "Explain the concept of gradient descent.", "model_answer": "Gradient descent is an optimization algorithm used to minimize the cost function by adjusting model parameters."},
    {"question": "What is a neural network?", "model_answer": "A neural network is a machine learning model that mimics the human brain, consisting of layers of nodes that process input data."}
]

# --- Similarity Scoring Stub (You can improve with cosine similarity etc.) ---
from difflib import SequenceMatcher
def grade_answer(model_answer, student_answer):
    similarity = SequenceMatcher(None, model_answer.lower(), student_answer.lower()).ratio()
    score = round(similarity * 5)  # Score out of 5
    return score, similarity

# --- LLaMA Feedback Function ---
def get_llama_feedback(model_answer, student_answer):
    headers = {
        "Authorization": f"Bearer {LLAMA_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": LLAMA_MODEL,
        "messages": [
            {"role": "user", "content": f"You are an AI assistant grading a student's answer.\n\nModel Answer:\n{model_answer}\n\nStudent Answer:\n{student_answer}\n\nGive a short analysis pointing out what's missing and how it can be improved."}
        ],
        "max_tokens": 150,
    }

    try:
        response = requests.post(LLAMA_API_URL, headers=headers, json=payload)
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"LLAMA API error: {e}"

# --- UI START ---
st.title("📘 AutoGrader AI - Powered by LLaMA via OpenRouter 🦙")
st.markdown("Upload a CSV with answers (Name, Q1, Q2, Q3, Q4, Q5) for batch grading & AI feedback.")

uploaded_file = st.file_uploader("📤 Upload student answers CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    output_data = []

    with st.spinner("Grading..."):
        for index, row in df.iterrows():
            student_name = row['Name']
            total_score = 0
            row_result = {"Name": student_name}

            for i, q in enumerate(questions):
                q_key = f"Q{i+1}"
                if q_key not in row:
                    continue
                student_answer = row[q_key]
                score, similarity = grade_answer(q['model_answer'], student_answer)
                feedback = get_llama_feedback(q['model_answer'], student_answer)

                row_result[f"{q_key}_Score"] = score
                row_result[f"{q_key}_Similarity"] = round(similarity, 2)
                row_result[f"{q_key}_Feedback"] = feedback
                total_score += score

            row_result["Total_Score"] = total_score
            output_data.append(row_result)

    output_df = pd.DataFrame(output_data)
    st.success("✅ Grading complete!")
    st.dataframe(output_df)

    csv = output_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Results CSV", data=csv, file_name="graded_results.csv", mime="text/csv")
