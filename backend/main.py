# import FastAPI tools
from fastapi import FastAPI, UploadFile, File

# import PDF reader
import PyPDF2

# import re
import re

# create the app
app = FastAPI()

# homepage route
@app.get("/")
def home():
    return {"message": "AI Resume Screener is running"}


# simple function to extract skills from text
def extract_skills(text):
    
    # basic list of skills to look for
    skills_list = [
        "python", "java", "c++", "c", "javascript",
        "sql", "machine learning", "data structures",
        "algorithms", "react", "fastapi"
    ]

    found_skills = []

    # check if each skill is in the resume text
    for skill in skills_list:
        if re.search(rf"\b{skill}\b", text.lower()):
            found_skills.append(skill)

    return found_skills


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

    # 🔥 use the skill extraction function
    skills = extract_skills(resume_text)

    # return both skills + preview
    return {
        "skills_found": skills,
        "preview": resume_text[:300]
    }