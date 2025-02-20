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

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += str(page.extract_text())
    return text

# ✅ Corrected Prompt Template (No extra indentation)
prompt_template = """Act as an **advanced ATS (Applicant Tracking System) specialist** with deep expertise in:
- **Technical fields**
- **Software engineering**
- **Data science**
- **Data analysis**
- **Big data engineering**

### **🔍 Your Task**
Analyze the provided resume against the given job description (JD). The job market is highly competitive, so your evaluation must be **accurate and actionable**.

### **📌 Evaluation Criteria**
1️⃣ **JD Match Percentage** – Calculate how well the resume aligns with the job description (**0-100%**).  
2️⃣ **Missing Keywords** – Identify **critical keywords and technical skills missing** from the resume but present in the JD.  
3️⃣ **Profile Summary & Resume Improvement Suggestions** – Provide a **detailed, structured analysis** covering:
   - Key **strengths** of the resume in relation to the JD.
   - **Weaknesses and potential ATS rejection reasons**.
   - **Actionable, specific recommendations** to optimize the resume for **higher ATS scoring**.

### **📌 Response Format**
Return the output **strictly as a JSON object** (without extra text, explanations, or formatting issues):

```json
{{
    "JD Match": "XX%", 
    "MissingKeywords": ["Keyword1", "Keyword2", "Keyword3"],
    "Profile Summary": "Comprehensive evaluation of strengths, weaknesses, and improvements."
}}
