"""Symptom First-Aid Agent - Provides general first-aid guidance with fallback"""
import json
from tools.gemini_client import generate_content

SYMPTOM_FIRSTAID_PROMPT = """You are a general first-aid information assistant.

STRICT SAFETY RULES:
❌ Do NOT diagnose any disease or condition
❌ Do NOT name specific diseases
❌ Do NOT recommend medicines
❌ Do NOT replace professional medical advice
✅ Only provide general first-aid information
✅ Always recommend consulting a doctor
✅ Focus on immediate comfort measures

User symptoms: {symptoms}

Provide response in this JSON format:
{{
    "possible_general_causes": ["Dehydration", "Fatigue", "Stress"],
    "first_aid_steps": {{
        "english": ["Rest in a comfortable position", "Drink small sips of water"],
        "kannada": ["ಆರಾಮದಾಯಕ ಸ್ಥಾನದಲ್ಲಿ ವಿಶ್ರಾಂತಿ ಪಡೆಯಿರಿ", "ಸಣ್ಣ ಗುಟುಕುಗಳಲ್ಲಿ ನೀರು ಕುಡಿಯಿರಿ"],
        "hindi": ["आरामदायक स्थिति में आराम करें", "पानी की छोटी-छोटी घूंट पिएं"]
    }},
    "things_to_avoid": {{
        "english": ["Avoid sudden movements", "Avoid heavy meals"],
        "kannada": ["ಹಠಾತ್ ಚಲನೆಗಳನ್ನು ತಪ್ಪಿಸಿ", "ಭಾರೀ ಊಟವನ್ನು ತಪ್ಪಿಸಿ"],
        "hindi": ["अचानक हलचल से बचें", "भारी भोजन से बचें"]
    }},
    "red_flags_see_doctor": {{
        "english": ["If symptoms persist more than 24 hours", "If you experience severe pain"],
        "kannada": ["ಲಕ್ಷಣಗಳು 24 ಗಂಟೆಗಳಿಗಿಂತ ಹೆಚ್ಚು ಇದ್ದರೆ", "ತೀವ್ರ ನೋವು ಇದ್ದರೆ"],
        "hindi": ["यदि लक्षण 24 घंटे से अधिक रहें", "यदि गंभीर दर्द हो"]
    }},
    "disclaimer": {{
        "english": "This is general first-aid information only. NOT medical advice. Please consult a doctor.",
        "kannada": "ಇದು ಸಾಮಾನ್ಯ ಪ್ರಥಮ ಚಿಕಿತ್ಸಾ ಮಾಹಿತಿ ಮಾತ್ರ. ವೈದ್ಯಕೀಯ ಸಲಹೆ ಅಲ್ಲ. ದಯವಿಟ್ಟು ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
        "hindi": "यह केवल सामान्य प्राथमिक चिकित्सा जानकारी है। चिकित्सा सलाह नहीं। कृपया डॉक्टर से परामर्श लें।"
    }}
}}

Remember: You are NOT diagnosing. Only providing comfort measures."""


def get_firstaid_guidance(symptoms: str) -> dict:
    """Get first-aid guidance for symptoms (NO diagnosis)"""
    
    prompt = SYMPTOM_FIRSTAID_PROMPT.format(symptoms=symptoms)
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
