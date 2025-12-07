"""Doctor Comparator Agent - Compares doctor opinions with fallback"""
import json
from tools.gemini_client import generate_content

DOCTOR_COMPARE_PROMPT = """You are a medical opinion comparison assistant.

STRICT SAFETY RULES:
❌ Do NOT recommend which doctor to follow
❌ Do NOT make medical decisions
❌ Do NOT say one opinion is "better" than another
✅ Only find COMMON points across opinions
✅ Only highlight DIFFERENCES objectively
✅ Let the user discuss with their doctors

Doctor opinions to compare:
{opinions}

Provide response in this JSON format:
{{
    "number_of_opinions": 3,
    "common_points": {{
        "english": ["All doctors recommend regular monitoring", "All suggest dietary changes"],
        "kannada": ["ಎಲ್ಲಾ ವೈದ್ಯರು ನಿಯಮಿತ ಮೇಲ್ವಿಚಾರಣೆ ಶಿಫಾರಸು ಮಾಡುತ್ತಾರೆ"],
        "hindi": ["सभी डॉक्टर नियमित निगरानी की सलाह देते हैं"]
    }},
    "differences": {{
        "english": ["Doctor 1 suggests medication A, Doctor 2 suggests medication B"],
        "kannada": ["ವೈದ್ಯ 1 ಔಷಧ A ಸೂಚಿಸುತ್ತಾರೆ, ವೈದ್ಯ 2 ಔಷಧ B ಸೂಚಿಸುತ್ತಾರೆ"],
        "hindi": ["डॉक्टर 1 दवा A सुझाते हैं, डॉक्टर 2 दवा B सुझाते हैं"]
    }},
    "most_consistent_advice": {{
        "english": "Based on agreement: Regular follow-up and lifestyle changes are commonly recommended.",
        "kannada": "ಒಮ್ಮತದ ಆಧಾರದ ಮೇಲೆ: ನಿಯಮಿತ ಅನುಸರಣೆ ಶಿಫಾರಸು ಮಾಡಲಾಗುತ್ತದೆ.",
        "hindi": "सहमति के आधार पर: नियमित फॉलो-अप सुझाए जाते हैं।"
    }},
    "questions_to_ask_doctors": {{
        "english": ["Why do treatment durations differ?"],
        "kannada": ["ಚಿಕಿತ್ಸೆಯ ಅವಧಿಗಳು ಏಕೆ ಭಿನ್ನವಾಗಿವೆ?"],
        "hindi": ["उपचार अवधि अलग क्यों है?"]
    }},
    "disclaimer": {{
        "english": "This comparison is for information only. Please discuss all options with your doctor.",
        "kannada": "ಈ ಹೋಲಿಕೆ ಮಾಹಿತಿಗಾಗಿ ಮಾತ್ರ. ನಿಮ್ಮ ವೈದ್ಯರೊಂದಿಗೆ ಚರ್ಚಿಸಿ.",
        "hindi": "यह तुलना केवल जानकारी के लिए है। अपने डॉक्टर से चर्चा करें।"
    }}
}}

Be objective. No recommendations. Only comparison."""


def compare_doctor_opinions(opinions: list) -> dict:
    """Compare 2-4 doctor opinions objectively"""
    
    formatted_opinions = "\n".join([f"Doctor {i+1}: {op}" for i, op in enumerate(opinions)])
    prompt = DOCTOR_COMPARE_PROMPT.format(opinions=formatted_opinions)
    response, model_used = generate_content(prompt)
    
    try:
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        result = json.loads(text.strip())
        result["_model_used"] = model_used
        return result
    except:
        return {"raw_response": response.text, "error": "Could not parse JSON", "_model_used": model_used}
