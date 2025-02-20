import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure Google Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get AI response
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    
    try:
        # Ensure valid JSON output
        json_response = json.loads(response.text)
    except json.JSONDecodeError:
        st.error("❌ Error: Received an invalid JSON response. Please check AI output format.")
        return None  # Return None if JSON parsing fails

    return json_response

# Function to extract text from PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += str(page.extract_text())
    return text

# AI Prompt Template
input_prompt = """
Hey, act as an **advanced ATS (Applicant Tracking System)** with deep expertise in:
- **Software Engineering**
- **Data Science**
- **Data Analytics**
- **Big Data Engineering**

### **Your Task**:
Analyze the following resume based on the given job description. The job market is highly competitive, so provide **precise and actionable feedback** to improve the resume’s ATS score.

---

### **🔍 Evaluation Criteria:**
🔹 **JD Match Percentage** – Calculate how well the resume matches the job description (**0-100%**).  
🔹 **Missing Keywords** – List important **keywords/skills missing** that would improve ATS compatibility.  
🔹 **Profile Summary & Improvement Suggestions** – Provide a **detailed analysis** covering:
   - Key **strengths** of the resume in relation to the job description.
   - **Weaknesses** that might cause rejection by an ATS.
   - **Actionable suggestions** to optimize the resume for **better ATS scoring**.

---

### **📌 Response Format (Strictly Follow This)**
Return the response **only in valid JSON format** like below:
```json
{{
  "JD Match": "XX%", 
  "MissingKeywords": ["Keyword1", "Keyword2", "Keyword3"],
  "Profile Summary": "Detailed resume analysis."
}}
