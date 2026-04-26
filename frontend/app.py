import streamlit as st
import pandas as pd

from frontend.api import rank_resumes
from frontend.components import (
    create_summary_dataframe,
    show_ranking_summary_table,
    show_skill_tags
)
from frontend.utils import clean_list, get_score_label

st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide"
)

st.title("AI Resume Screener")

st.write(
    "Upload one or more resumes and paste a job description to rank candidates "
    "based on how well their skills match the role."
)

resume_files = st.file_uploader(
    "Upload resume PDF(s)",
    type=["pdf"],
    accept_multiple_files=True
)

job_description = st.text_area(
    "Paste job description",
    height=250,
    placeholder="Paste the full job description here for better matching results..."
)

if st.button("Analyze Resume(s)"):

    if not resume_files or job_description.strip() == "":
        st.error("Please upload at least one resume and paste a job description.")
    else:

        with st.spinner("Analyzing resumes... This may take a moment."):
            response = rank_resumes(resume_files, job_description)

        if response.status_code == 200:
            result = response.json()
            ranked_resumes = result["ranked_resumes"]

            st.success("Resume analysis complete.")

            st.header("Resume Ranking Summary")

            summary_df = create_summary_dataframe(ranked_resumes)

            show_ranking_summary_table(summary_df)

            csv_data = summary_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download Results as CSV",
                data=csv_data,
                file_name="resume_ranking_results.csv",
                mime="text/csv"
            )

            st.divider()

            st.header("Detailed Resume Results")

            for i, resume in enumerate(ranked_resumes, 1):
                match = resume.get("match_result", {})
                score = resume.get("score", 0)
                filename = resume.get("filename", "Unknown file")

                with st.expander(
                    f"#{i} - {filename} | {score}% Match",
                    expanded=(i == 1)
                ):

                    col1, col2, col3 = st.columns([1, 1, 1])

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