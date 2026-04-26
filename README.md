# AI Resume Screener

AI Resume Screener is a Python web application that helps compare and rank resume PDFs against a job description. Users can upload one or more resumes, paste a job description, and receive ranked results based on skill match, missing skills, score breakdown, and improvement advice.

## Features

- Upload one or more resume PDFs
- Paste a job description for comparison
- Extract technical skills from resumes
- Use AI to compare resume content against the job description
- Rank multiple resumes by match score
- View detailed analysis for each resume
- See matching skills, missing skills, and score breakdowns
- Download ranked results as a CSV file

## Tech Stack

- Python
- FastAPI
- Streamlit
- OpenAI API
- PyPDF2
- Pandas
- Requests

## Project Structure

```text
AI-RESUME-SCREENER/
│
├── backend/
│   ├── main.py
│   ├── matcher.py
│   ├── pdf_utils.py
│   ├── ranking.py
│   └── skill_extractor.py
│
├── frontend/
│   ├── app.py
│   ├── api.py
│   ├── components.py
│   └── utils.py
│
├── tests/
├── README.md
└── .gitignore