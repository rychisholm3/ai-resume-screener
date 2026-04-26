import requests

BACKEND_URL = "http://127.0.0.1:8000"


def rank_resumes(resume_files, job_description):
    files = []

    for resume_file in resume_files:
        files.append(
            (
                "files",
                (
                    resume_file.name,
                    resume_file.getvalue(),
                    "application/pdf"
                )
            )
        )

    data = {
        "job_description": job_description
    }

    response = requests.post(
        f"{BACKEND_URL}/rank",
        files=files,
        data=data
    )

    return response