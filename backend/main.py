# import FastAPI tools
from fastapi import FastAPI, UploadFile, File

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
    Return them as a clean comma-separated list.

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