import json


def clean_list(value):
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, str):
        cleaned_value = value.strip()

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


def get_score_label(score):
    if score >= 85:
        return "Strong Match"
    elif score >= 70:
        return "Good Match"
    elif score >= 50:
        return "Possible Match"
    else:
        return "Weak Match"