from fastapi import FastAPI, UploadFile, File, Form

from backend.pdf_utils import extract_text_from_pdf
from backend.skill_extractor import get_resume_skills
from backend.matcher import match_resume_to_job
from backend.ranking import rank_resume_files

app = FastAPI()


@app.get("/")
def home():
    return {"message": "AI Resume Screener is running"}


@app.post("/upload")
def upload_resume(file: UploadFile = File(...)):
    resume_text = extract_text_from_pdf(file)
    skills = get_resume_skills(resume_text)

    return {
        "skills_found": skills,
        "preview": resume_text[:300]
    }


@app.post("/analyze")
def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    resume_text = extract_text_from_pdf(file)
    skills = get_resume_skills(resume_text)
    match_result = match_resume_to_job(resume_text, skills, job_description)

    return {
        "skills_found": skills,
        "match_result": match_result
    }


@app.post("/rank")
def rank_resumes(
    files: list[UploadFile] = File(..., description="Upload one or more resume PDFs"),
    job_description: str = Form(...)
):
    ranked_results = rank_resume_files(files, job_description)

    return {
        "ranked_resumes": ranked_results
    }