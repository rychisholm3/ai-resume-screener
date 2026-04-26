# import tools for the frontend
import streamlit as st
import requests
import pandas as pd
import json

# backend URL
BACKEND_URL = "http://127.0.0.1:8000"

# page setup
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide"
)

# page title
st.title("AI Resume Screener")

# short description
st.write(
    "Upload one or more resumes and paste a job description to rank candidates "
    "based on how well their skills match the role."
)

# file uploader that allows multiple PDF files
resume_files = st.file_uploader(
    "Upload resume PDF(s)",
    type=["pdf"],
    accept_multiple_files=True
)

# job description input
job_description = st.text_area(
    "Paste job description",
    height=150,
    placeholder="Example: Computer Science Internship requiring Python, C++, Git, data structures..."
)


def clean_list(value):
    """
    Makes sure values display as lists instead of printing one character at a time.
    """
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, str):
        cleaned_value = value.strip()

        # Handles cases where the AI returns ```json ... ```
        if cleaned_value.startswith("```"):
            cleaned_value = cleaned_value.replace("```json", "")
            cleaned_value = cleaned_value.replace("```JSON", "")
            cleaned_value = cleaned_value.replace("```", "")
            cleaned_value = cleaned_value.strip()

        try:
            parsed_value = json.loads(cleaned_value)

            if isinstance(parsed_value, list):
                return parsed_value
        except Exception:
            pass

        return [cleaned_value]

    return []


def show_skill_tags(skills):
    """
    Display skills in a cleaner tag-like format instead of a raw printed list.
    """
    skills = clean_list(skills)

    if not skills:
        st.caption("No skills found.")
        return

    skill_html = ""

    for skill in skills:
        skill_html += f"""
        <span style="
            display: inline-block;
            padding: 6px 10px;
            margin: 4px;
            border-radius: 16px;
            background-color: #262730;
            border: 1px solid #444;
            font-size: 14px;
        ">
            {skill}
        </span>
        """

    st.markdown(skill_html, unsafe_allow_html=True)


def get_score_label(score):
    """
    Returns a simple label based on the resume match score.
    """
    if score >= 85:
        return "Strong Match"
    elif score >= 70:
        return "Good Match"
    elif score >= 50:
        return "Possible Match"
    else:
        return "Weak Match"


def create_summary_dataframe(ranked_resumes):
    """
    Creates the summary table used for both Streamlit display and CSV export.
    """
    summary_rows = []

    for i, resume in enumerate(ranked_resumes, 1):
        match = resume.get("match_result", {})
        score = resume.get("score", 0)

        matching_skills = clean_list(match.get("matching_skills", []))
        missing_skills = clean_list(match.get("missing_skills", []))

        summary_rows.append({
            "Rank": i,
            "Filename": resume.get("filename", "Unknown"),
            "Score": score,
            "Match Level": get_score_label(score),
            "Matching Skills": ", ".join(matching_skills),
            "Missing Skills": ", ".join(missing_skills),
            "Summary": match.get("summary", "")
        })

    return pd.DataFrame(summary_rows)


# analyze button
if st.button("Analyze Resume(s)"):

    # make sure both inputs are provided
    if not resume_files or job_description.strip() == "":
        st.error("Please upload at least one resume and paste a job description.")
    else:
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

        with st.spinner("Analyzing resumes... This may take a moment."):
            response = requests.post(
                f"{BACKEND_URL}/rank",
                files=files,
                data=data
            )

        if response.status_code == 200:
            result = response.json()
            ranked_resumes = result["ranked_resumes"]

            st.success("Resume analysis complete.")

            st.header("Resume Ranking Summary")

            # create a clean summary table
            summary_df = create_summary_dataframe(ranked_resumes)

            # show shorter version on the website
            display_df = summary_df.copy()

            display_df["Score"] = display_df["Score"].astype(str) + "%"

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )

            # CSV download button
            csv_data = summary_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download Results as CSV",
                data=csv_data,
                file_name="resume_ranking_results.csv",
                mime="text/csv"
            )

            st.divider()

            st.header("Detailed Resume Results")

            # show detailed results in expanders
            for i, resume in enumerate(ranked_resumes, 1):
                match = resume.get("match_result", {})
                score = resume.get("score", 0)
                filename = resume.get("filename", "Unknown file")

                with st.expander(
                    f"#{i} - {filename} | {score}% Match",
                    expanded=(i == 1)
                ):

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Match Score", f"{score}%")

                    with col2:
                        st.metric("Match Level", get_score_label(score))

                    with col3:
                        matching_count = len(
                            clean_list(match.get("matching_skills", []))
                        )
                        st.metric("Matching Skills", matching_count)

                    st.subheader("Summary")
                    st.write(match.get("summary", "No summary available."))

                    st.subheader("Skills Found in Resume")
                    show_skill_tags(resume.get("skills_found", []))

                    st.subheader("Matching Skills")
                    show_skill_tags(match.get("matching_skills", []))

                    st.subheader("Missing Skills")
                    show_skill_tags(match.get("missing_skills", []))

                    st.subheader("Score Breakdown")

                    score_breakdown = match.get("score_breakdown", {})

                    if score_breakdown:
                        breakdown_df = pd.DataFrame(
                            list(score_breakdown.items()),
                            columns=["Category", "Score"]
                        )

                        st.dataframe(
                            breakdown_df,
                            use_container_width=True,
                            hide_index=True
                        )
                    else:
                        st.caption("No score breakdown available.")

                    st.subheader("Improvement Advice")

                    improvement_advice = clean_list(
                        match.get("improvement_advice", [])
                    )

                    if improvement_advice:
                        for advice in improvement_advice:
                            st.write(f"- {advice}")
                    else:
                        st.caption("No improvement advice available.")

                    st.subheader("Resume Suggestions")

                    resume_suggestions = clean_list(
                        match.get("resume_suggestions", [])
                    )

                    if resume_suggestions:
                        for suggestion in resume_suggestions:
                            st.write(f"- {suggestion}")
                    else:
                        st.caption("No resume suggestions available.")

        else:
            st.error("Something went wrong while analyzing the resumes.")
            st.write(response.text)