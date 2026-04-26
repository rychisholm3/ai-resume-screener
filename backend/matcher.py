import json
from openai import OpenAI

client = OpenAI()


def clean_ai_json_response(text):
    """
    Cleans the AI response so it can be parsed as JSON.
    """
    if text is None:
        return ""

    cleaned_text = text.strip()

    if cleaned_text.startswith("```"):
        cleaned_text = cleaned_text.replace("```json", "")
        cleaned_text = cleaned_text.replace("```JSON", "")
        cleaned_text = cleaned_text.replace("```", "")
        cleaned_text = cleaned_text.strip()

    start_index = cleaned_text.find("{")
    end_index = cleaned_text.rfind("}")

    if start_index != -1 and end_index != -1:
        cleaned_text = cleaned_text[start_index:end_index + 1]

    return cleaned_text


def match_resume_to_job(resume_text, resume_skills, job_description):
    prompt = f"""
    You are an AI resume screening assistant.

    Compare this resume to the job description.

    IMPORTANT RULES:
    - Use the resume text and extracted skills when judging the candidate.
    - If the job description is short or vague, still evaluate it based on the role described.
    - Do not invent skills that are not in the resume.
    - Matching skills should be skills or experience from the resume that are useful for the job.
    - Missing skills should be important skills or concepts for the job that are not clearly shown in the resume.
    - Give a realistic match score from 0 to 100.
    - A resume can still get partial credit for related skills.
    - For example, Python, data structures, algorithms, and programming experience are useful for AI or CS internship roles.
    - If the score is below 85, give specific improvement advice.
    - Keep advice practical and specific.

    Resume text:
    {resume_text}

    Extracted resume skills:
    {resume_skills}

    Job description:
    {job_description}

    Return ONLY valid JSON in this exact format:

    {{
        "match_score": 0,
        "score_breakdown": {{
            "technical_skills": 0,
            "tools": 0,
            "experience": 0
        }},
        "matching_skills": [],
        "missing_skills": [],
        "summary": "",
        "improvement_advice": [],
        "resume_suggestions": []
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message.content
    cleaned_result = clean_ai_json_response(result)

    try:
        return json.loads(cleaned_result)
    except Exception:
        return {
            "match_score": 0,
            "score_breakdown": {
                "technical_skills": 0,
                "tools": 0,
                "experience": 0
            },
            "matching_skills": [],
            "missing_skills": [],
            "summary": "The AI response could not be parsed correctly.",
            "improvement_advice": [],
            "resume_suggestions": [],
            "raw_output": result
        }