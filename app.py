import streamlit as st
import io
import os
import base64
import pdf2image
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import PyPDF2  # replaced PyPDF2streamlit

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini API
if not api_key:
    st.error("API key is missing! Please set GOOGLE_API_KEY in your .env file.")
else:
    genai.configure(api_key=api_key)

# -----------------------------
# Function to extract PDF first page and convert to image (for Gemini Vision)
# -----------------------------
def input_pdf_setup(uploaded_file):
    try:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }]
        return pdf_parts
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

# -----------------------------
# Function to generate response using Gemini
# -----------------------------
def get_gemini_response(job_desc, pdf_content, prompt):
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(
            contents=[
                {"text": job_desc},
                pdf_content[0],
                {"text": prompt}
            ]
        )
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="ATS Resume Checker")
st.title("🚀 Application Tracking System (ATS) Resume Checker")

input_text = st.text_area("Job Description", placeholder="Paste the job description here")
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    st.success("✅ Resume uploaded successfully!")

analyze_resume = st.button("🔍 Analyze My Resume")
match_resume = st.button("📊 Match My Resume With JD")

# -----------------------------
# Prompts for AI
# -----------------------------
input_prompt1 = """
You are an experienced Technical HR Manager. Review the provided resume against the job description.
Highlight strengths, weaknesses, relevance, and hiring decision perspective.
"""

input_prompt2 = """
You are an ATS (Applicant Tracking System) Analyzer.
Evaluate the resume vs the job description.
Provide:
1️⃣ Match Percentage
2️⃣ Missing Keywords
3️⃣ Final Hiring Recommendation
"""

# -----------------------------
# Button Logic
# -----------------------------
if analyze_resume:
    if uploaded_file is not None and input_text:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:
            response = get_gemini_response(input_text, pdf_content, input_prompt1)
            st.subheader("📄 Resume Evaluation:")
            st.write(response)
    else:
        st.error("⚠️ Please upload a resume and provide a job description.")

if match_resume:
    if uploaded_file is not None and input_text:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:
            response = get_gemini_response(input_text, pdf_content, input_prompt2)
            st.subheader("📊 Match Percentage & Missing Keywords:")
            st.write(response)
    else:
        st.error("⚠️ Please upload a resume and provide a job description.")
