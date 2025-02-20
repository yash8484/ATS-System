import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv


load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Hey, act as an **advanced ATS (Applicant Tracking System) specialist** with deep expertise in:
- **Technical fields**
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
Use **bold headings** for each section.  
**Keep it structured, concise, and highly analytical.**  
**Do NOT add unnecessary explanations.**  

---
### ** Resume for Evaluation:**
{text}

### ** Job Description:**
{jd}

I want the response in this structure

"JD Match":"%",

"MissingKeywords:[]",

"Profile Summary":""}}



"""

## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        st.subheader(response)