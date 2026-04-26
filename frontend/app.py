# import tools for the frontend
import streamlit as st
import requests

# page title
st.title("AI Resume Screener")

# short description
st.write("Upload a resume and paste a job description to get an AI match score.")

# file uploader
resume_file = st.file_uploader("Upload resume PDF", type=["pdf"])

# job description input
job_description = st.text_area("Paste job description")

# analyze button
if st.button("Analyze Resume"):

    # make sure both inputs are provided
    if resume_file is None or job_description.strip() == "":
        st.error("Please upload a resume and paste a job description.")
    else:
        # send the resume and job description to the backend
        files = {
            "file": (resume_file.name, resume_file, "application/pdf")
        }

        data = {
            "job_description": job_description
        }

        response = requests.post(
            "http://127.0.0.1:8000/analyze",
            files=files,
            data=data
        )

        # show the result
        if response.status_code == 200:
            result = response.json()

            st.subheader("Skills Found")
            st.write(result["skills_found"])

            match = result["match_result"]

            st.metric("Match Score", f"{match['match_score']}%")

            st.subheader("Matching Skills")
            st.write(match["matching_skills"])

            st.subheader("Missing Skills")
            st.write(match["missing_skills"])

            st.subheader("Summary")
            st.write(match["summary"])

            st.subheader("Improvement Advice")
            st.write(match.get("improvement_advice", []))

            st.subheader("Resume Suggestions")
            st.write(match.get("resume_suggestions", []))

        else:
            st.error("Something went wrong.")