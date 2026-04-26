# import tools for the frontend
import streamlit as st
import requests

# page title
st.title("AI Resume Screener")

# short description
st.write("Upload one or more resumes and paste a job description to get AI match scores.")

# file uploader that allows multiple PDF files
resume_files = st.file_uploader(
    "Upload resume PDF(s)",
    type=["pdf"],
    accept_multiple_files=True
)

# job description input
job_description = st.text_area("Paste job description")

# analyze button
if st.button("Analyze Resume(s)"):

    # make sure both inputs are provided
    if not resume_files or job_description.strip() == "":
        st.error("Please upload at least one resume and paste a job description.")
    else:
        # send all resumes and the job description to the backend
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
            "http://127.0.0.1:8000/rank",
            files=files,
            data=data
        )

        # show the result
        if response.status_code == 200:
            result = response.json()

            st.subheader("Ranked Resumes")

            for i, resume in enumerate(result["ranked_resumes"], 1):
                st.divider()

                st.subheader(f"#{i} - {resume['filename']}")
                st.metric("Match Score", f"{resume['score']}%")

                st.subheader("Skills Found")
                st.write(resume["skills_found"])

                match = resume["match_result"]

                st.subheader("Matching Skills")
                st.write(match.get("matching_skills", []))

                st.subheader("Missing Skills")
                st.write(match.get("missing_skills", []))

                st.subheader("Summary")
                st.write(match.get("summary", ""))

                st.subheader("Score Breakdown")
                st.json(match.get("score_breakdown", {}))

                st.subheader("Improvement Advice")
                st.write(match.get("improvement_advice", []))

                st.subheader("Resume Suggestions")
                st.write(match.get("resume_suggestions", []))

        else:
            st.error("Something went wrong.")
            st.write(response.text)