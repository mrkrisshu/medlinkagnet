"""Doctor Recommender Agent - Suggests specialist type + nearby doctors"""
import json
from tools.gemini_client import generate_content

DOCTOR_RECOMMEND_PROMPT = """You are a healthcare navigation assistant.

SAFETY RULES:
❌ Do NOT diagnose diseases
❌ Do NOT prescribe treatments
✅ Only suggest TYPES of specialists based on symptoms/reports
✅ Always recommend consulting a doctor first

Based on this information: {info}

Suggest which type of specialist the user should consult.

Return JSON:
{{
    "recommended_specialists": [
        {{
            "type": "Hematologist",
            "reason": {{
                "english": "Low hemoglobin may require blood specialist evaluation",
                "kannada": "ಕಡಿಮೆ ಹಿಮೋಗ್ಲೋಬಿನ್ ರಕ್ತ ತಜ್ಞರ ಮೌಲ್ಯಮಾಪನ ಅಗತ್ಯವಿರಬಹುದು",
                "hindi": "कम हीमोग्लोबिन के लिए रक्त विशेषज्ञ की जांच आवश्यक हो सकती है"
            }},
            "urgency": "routine/soon/urgent"
        }}
    ],
    "primary_recommendation": {{
        "specialist": "General Physician",
        "reason": {{
            "english": "Start with a general checkup first",
            "kannada": "ಮೊದಲು ಸಾಮಾನ್ಯ ತಪಾಸಣೆಯಿಂದ ಪ್ರಾರಂಭಿಸಿ",
            "hindi": "पहले सामान्य जांच से शुरू करें"
        }}
    }},
    "google_maps_search_terms": [
        "Hematologist near me",
        "Blood specialist doctor",
        "General physician near me"
    ],
    "disclaimer": {{
        "english": "This is a suggestion only. Please consult your family doctor first.",
        "kannada": "ಇದು ಕೇವಲ ಸಲಹೆ. ದಯವಿಟ್ಟು ಮೊದಲು ನಿಮ್ಮ ಕುಟುಂಬ ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
        "hindi": "यह केवल सुझाव है। कृपया पहले अपने पारिवारिक डॉक्टर से परामर्श लें।"
    }}
}}

Be helpful but always recommend professional consultation."""


def recommend_doctor(info: str) -> dict:
    """Recommend specialist type based on symptoms/report"""
    
    prompt = DOCTOR_RECOMMEND_PROMPT.format(info=info)
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


def get_google_maps_link(search_term: str) -> str:
    """Generate Google Maps search link for nearby doctors"""
    import urllib.parse
    encoded = urllib.parse.quote(search_term)
    return f"https://www.google.com/maps/search/{encoded}"
