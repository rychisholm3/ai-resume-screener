from backend.pdf_utils import extract_text_from_pdf
from backend.skill_extractor import get_resume_skills
from backend.matcher import match_resume_to_job


def rank_resume_files(files, job_description):
    ranked_results = []

    for file in files:
        resume_text = extract_text_from_pdf(file)
        skills = get_resume_skills(resume_text)
        match_result = match_resume_to_job(skills, job_description)

        score = match_result.get("match_score", 0)

        ranked_results.append({
            "filename": file.filename,
            "score": score,
            "skills_found": skills,
            "match_result": match_result
        })

    ranked_results.sort(key=lambda result: result["score"], reverse=True)

    return ranked_results