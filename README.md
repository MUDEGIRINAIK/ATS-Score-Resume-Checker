# ATS Resume Checker

This project is an **Application Tracking System (ATS) Resume Checker** built using **Python**, **Streamlit**, and **Google Generative AI**. It allows users to upload resumes in PDF format and compare them with job descriptions to receive AI-powered evaluations, such as professional feedback and a percentage match.

## Features

- **Resume Upload**: Upload your resume in PDF format.
- **AI-Powered Analysis**: Google Gen AI (Gemini model) provides a detailed professional evaluation of your resume, highlighting strengths and weaknesses based on the job description.
- **ATS Percentage Match**: The system also calculates the percentage match of the resume against the provided job description and highlights any missing keywords.

## Tech Stack

- **Streamlit**: For building the web app interface.
- **Python**: The core logic and processing.
- **Google Generative AI (Gemini Model)**: Used to provide intelligent feedback and resume analysis.
- **pdf2image**: For converting PDF resumes into images for AI processing.
- **PIL**: Used to handle image manipulation.
- **dotenv**: For securely managing API keys.

## Usage

- **Run the Streamlit App**: streamlit run app.py
- **Upload Your Resume**: On the web interface, input a job description in the text area. And upload your resume in PDF format.
- **Analyze Your Resume**: Click the Analyze My Resume button to get a professional evaluation of your resume based on the provided job description.
- **Match Percentage**: Click the Match My Resume With The JD button to get the percentage match of your resume with the job description, along with missing keywords.


   
