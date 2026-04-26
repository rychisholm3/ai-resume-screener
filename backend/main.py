# import FastAPI tools
from fastapi import FastAPI, UploadFile, File, Form

# import PDF reader
import PyPDF2

# import regex
import re

# import OpenAI
from openai import OpenAI

# create OpenAI client
client = OpenAI()

# create the app
app = FastAPI()

# import jason
import json

# homepage route
@app.get("/")
def home():
    return {"message": "AI Resume Screener is running"}


# simple function to extract skills (fallback method)
def extract_skills(text):
    
    skills_list = [
        "python", "java", "c++", "c", "javascript",
        "sql", "machine learning", "data structures",
        "algorithms", "react", "fastapi"
    ]

    found_skills = []

    for skill in skills_list:
        if re.search(rf"\b{skill}\b", text.lower()):
            found_skills.append(skill)

    return found_skills


# AI-powered skill extraction
def extract_skills_ai(text):
    
    prompt = f"""
    Extract all technical skills from this resume.

    Return ONLY a Python list.
    Example:
    ["Python", "C++", "SQL"]

    Resume:
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# route for uploading a resume PDF
@app.post("/upload")
def upload_resume(file: UploadFile = File(...)):

    # read the uploaded PDF
    pdf_reader = PyPDF2.PdfReader(file.file)

    resume_text = ""

    # extract text from each page
    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            resume_text += page_text + "\n"

    # 🔥 try AI first
    try:
        skills = extract_skills_ai(resume_text)
    except Exception:
        # fallback if AI fails
        skills = extract_skills(resume_text)

    return {
        "skills_found": skills,
        "preview": resume_text[:300]
    }

# compare resume skills to the job description
def match_resume_to_job(resume_skills, job_description):

    prompt = f"""
    You are an AI resume screening assistant.

    Compare the resume skills to the job description.

    Resume skills:
    {resume_skills}

    Job description:
    {job_description}

    Return ONLY valid JSON in this format:

    {{
    "match_score": number,
    "matching_skills": [],
    "missing_skills": [],
    "summary": ""
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message.content

    try:
        return json.loads(result)
    except:
        return {"raw_output": result}

# route for analyzing a resume against a job description
@app.post("/analyze")
def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    # read the uploaded PDF
    pdf_reader = PyPDF2.PdfReader(file.file)

    resume_text = ""

    # extract text from each page
    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            resume_text += page_text + "\n"

    # extract skills from the resume
    try:
        skills = extract_skills_ai(resume_text)
    except Exception:
        skills = extract_skills(resume_text)

    # compare resume to job description
    match_result = match_resume_to_job(skills, job_description)

    return {
        "skills_found": skills,
        "match_result": match_result
    }