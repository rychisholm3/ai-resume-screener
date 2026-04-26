import json
import re
from openai import OpenAI

client = OpenAI()


def extract_skills(text):
    skills_list = [
        "python", "java", "c++", "c", "javascript",
        "sql", "machine learning", "data structures",
        "algorithms", "react", "fastapi"
    ]

    found_skills = []

    for skill in skills_list:
        if re.search(rf"\b{skill}\b", text.lower()):
            found_skills.append(skill)

    return found_skills


def extract_skills_ai(text):
    prompt = f"""
    Extract all technical skills from this resume.

    Return ONLY valid JSON as a list.
    Example:
    ["Python", "C++", "SQL"]

    Resume:
    {text}
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
        return result


def get_resume_skills(resume_text):
    try:
        return extract_skills_ai(resume_text)
    except Exception:
        return extract_skills(resume_text)