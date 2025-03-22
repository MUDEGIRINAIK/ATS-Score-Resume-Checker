import streamlit as st # type: ignore
import io
import os
import base64
import pdf2image # type: ignore
import google.generativeai as genai # type: ignore
from PIL import Image # type: ignore
from dotenv import load_dotenv # type: ignore

# Load environment variables from .env file
#load_dotenv()

# Configure Google Generative AI with the API key from the environment
#genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Load environment variables from .env file
load_dotenv()

# Fetch API key from environment
api_key = os.getenv("GOOGLE_API_KEY")

# Check if API key is available
if not api_key:
    st.error("API key is missing! Please check your .env file or set GOOGLE_API_KEY manually.")
else:
    genai.configure(api_key=api_key)


# Function to get a response from Google Generative AI
def get_gemini_response(job_desc, pdf_content, prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([job_desc, pdf_content[0], prompt])
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Function to process PDF and convert to image for AI evaluation
def input_pdf_setup(uploaded_file):
    try:
        # Convert PDF to images (one image per page)
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        
        # Process only the first page for analysis
        first_page = images[0]

        # Convert the image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Convert image bytes to base64 encoding for AI processing
        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
        }]
        return pdf_parts
    except Exception as e:
        st.error(f"Error processing PDF file: {str(e)}")
        return None

# Streamlit app configuration
st.set_page_config(page_title="ATS Resume Checker")
st.title("🚀 Application Tracking System (ATS) Resume Checker")

# Job description input
input_text = st.text_area("Job Description", placeholder="Paste the job description here")

# File uploader for PDF resume
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

# Ensure the resume is uploaded successfully
if uploaded_file is not None:
    st.success("Resume uploaded successfully!")

# Define buttons for two different actions
analyze_resume = st.button("Analyze My Resume")
match_resume = st.button("Match My Resume With The JD")

# Prompt for professional analysis by HR Manager
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

# Prompt for ATS percentage match and missing keywords
input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Provide the match percentage and list missing keywords.
Conclude with final thoughts.
"""

# Action: Analyze Resume
if analyze_resume:
    if uploaded_file is not None and input_text:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:
            response = get_gemini_response(input_text, pdf_content, input_prompt1)
            st.subheader("📄 Detailed Analysis of Your Resume:")
            st.write(response)
    else:
        st.error("Please upload a resume and provide a job description.")

# Action: Match Resume with JD
if match_resume:
    if uploaded_file is not None and input_text:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:
            response = get_gemini_response(input_text, pdf_content, input_prompt2)
            st.subheader("📊 Match Percentage & Missing Keywords:")
            st.write(response)
    else:
        st.error("Please upload a resume and provide a job description.")
