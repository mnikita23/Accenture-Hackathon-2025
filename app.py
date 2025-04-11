# Job Screening Project using Ollama Phi Model

import os
import streamlit as st
from PyPDF2 import PdfReader
from ollama import Client

# Initialize Ollama client
ollama = Client()

# Helper function to read text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    except:
        text = "Could not read the PDF."
    return text

# Helper function to call Ollama Phi model
def evaluate_cv(cv_text, jd_text):
    prompt = f"""
    Given the following Job Description (JD):
    {jd_text}

    And the following CV:
    {cv_text}

    Score the CV out of 100 based on how well it matches the JD.
    Also, list the candidate's key strengths and weaknesses according to the JD.

    Provide output in this format:
    Score: <score>
    Strengths: <list>
    Weaknesses: <list>
    """

    response = ollama.chat(model="phi", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# UI setup
st.title("Job Screening with Ollama Phi")

jd_text = st.text_area("Paste Job Description", height=200)
uploaded_cvs = st.file_uploader("Upload CVs (Multiple PDFs)", type=["pdf"], accept_multiple_files=True)
threshold = st.slider("Set Scoring Threshold", 0, 100, 70)

if jd_text and uploaded_cvs:
    st.write("## CV Analysis Results")
    for cv_file in uploaded_cvs:
        cv_name = os.path.basename(cv_file.name)
        with st.spinner(f"Evaluating {cv_name}..."):
            cv_text = extract_text_from_pdf(cv_file)
            analysis = evaluate_cv(cv_text, jd_text)

            score_line = [line for line in analysis.split('\n') if line.startswith("Score")]
            try:
                score = float(score_line[0].split(":")[1].strip()) if score_line else 0
            except:
                score = 0

            st.markdown(f"### {cv_name} - Score: {round(score)}")
            st.text(analysis)

            if score >= threshold:
                st.success(f"Candidate meets the threshold! Score: {round(score)}")
                st.checkbox("Mark to send email to this candidate", key=cv_name)
            else:
                st.warning(f"Candidate does not meet the threshold. Score: {round(score)}")