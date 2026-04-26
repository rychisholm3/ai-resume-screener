import json
from openai import OpenAI

client = OpenAI()


def match_resume_to_job(resume_skills, job_description):
    prompt = f"""
    You are an AI resume screening assistant.

    Compare the resume skills to the job description.

    IMPORTANT RULES:
    - Only consider skills that appear in the job description
    - Do NOT invent or assume missing skills
    - Matching skills = skills in BOTH resume and job description
    - Missing skills = skills in job description BUT NOT in resume
    - If the score is below 85, give specific improvement advice
    - improvement_advice = skills or concepts the candidate should learn
    - resume_suggestions = ways to improve the resume wording for this job
    - Provide a score_breakdown with categories like technical_skills, tools, and experience
    - Keep advice practical and specific

    Resume skills:
    {resume_skills}

    Job description:
    {job_description}

    Return ONLY valid JSON in this format:

    {{
        "match_score": number,
        "score_breakdown": {{
            "technical_skills": number,
            "tools": number,
            "experience": number
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

    try:
        return json.loads(result)
    except:
        return {"raw_output": result}