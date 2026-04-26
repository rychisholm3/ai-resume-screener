import html
import pandas as pd
import streamlit as st

from frontend.utils import clean_list, get_score_label


def show_skill_tags(skills):
    skills = clean_list(skills)

    if not skills:
        st.caption("No skills found.")
        return

    skill_html = (
        '<div style="'
        'display: flex; '
        'flex-wrap: wrap; '
        'gap: 8px; '
        'margin-bottom: 8px;'
        '">'
    )

    for skill in skills:
        safe_skill = html.escape(str(skill))

        skill_html += (
            '<span style="'
            'display: inline-block; '
            'padding: 6px 12px; '
            'border-radius: 16px; '
            'background-color: #262730; '
            'border: 1px solid #444; '
            'font-size: 14px; '
            'white-space: nowrap;'
            '">'
            f'{safe_skill}'
            '</span>'
        )

    skill_html += '</div>'

    st.markdown(skill_html, unsafe_allow_html=True)


def create_summary_dataframe(ranked_resumes):
    summary_rows = []

    for i, resume in enumerate(ranked_resumes, 1):
        match = resume.get("match_result", {})
        score = resume.get("score", 0)

        summary_rows.append({
            "Rank": i,
            "Resume": resume.get("filename", "Unknown"),
            "Score": score,
            "Match Level": get_score_label(score),
            "Summary": match.get("summary", "")
        })

    return pd.DataFrame(summary_rows)


def show_ranking_summary_table(summary_df):
    table_html = (
        '<style>'
        '.summary-table {'
        'width: 100%;'
        'border-collapse: collapse;'
        'table-layout: fixed;'
        'margin-bottom: 12px;'
        'font-size: 14px;'
        '}'
        '.summary-table th {'
        'background-color: #1f2028;'
        'color: #d6d6d6;'
        'text-align: left;'
        'padding: 10px;'
        'border: 1px solid #333640;'
        'font-weight: 600;'
        '}'
        '.summary-table td {'
        'padding: 12px 10px;'
        'border: 1px solid #333640;'
        'vertical-align: top;'
        'line-height: 1.4;'
        'word-wrap: break-word;'
        'white-space: normal;'
        '}'
        '.rank-col {'
        'width: 55px;'
        'text-align: center;'
        '}'
        '.resume-col {'
        'width: 220px;'
        '}'
        '.score-col {'
        'width: 80px;'
        'text-align: center;'
        'font-weight: 600;'
        '}'
        '.match-col {'
        'width: 130px;'
        'font-weight: 600;'
        '}'
        '.summary-col {'
        'width: auto;'
        '}'
        '</style>'
        '<table class="summary-table">'
        '<thead>'
        '<tr>'
        '<th class="rank-col">Rank</th>'
        '<th class="resume-col">Resume</th>'
        '<th class="score-col">Score</th>'
        '<th class="match-col">Match Level</th>'
        '<th class="summary-col">Summary</th>'
        '</tr>'
        '</thead>'
        '<tbody>'
    )

    for _, row in summary_df.iterrows():
        rank = html.escape(str(row["Rank"]))
        resume = html.escape(str(row["Resume"]))
        score = html.escape(str(row["Score"]))
        match_level = html.escape(str(row["Match Level"]))
        summary = html.escape(str(row["Summary"]))

        table_html += (
            '<tr>'
            f'<td class="rank-col">{rank}</td>'
            f'<td class="resume-col">{resume}</td>'
            f'<td class="score-col">{score}%</td>'
            f'<td class="match-col">{match_level}</td>'
            f'<td class="summary-col">{summary}</td>'
            '</tr>'
        )

    table_html += '</tbody></table>'

    st.markdown(table_html, unsafe_allow_html=True)