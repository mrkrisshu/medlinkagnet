"""Medicine Safety Agent - Checks for drug interactions with fallback"""
import json
from tools.gemini_client import generate_content
from prompts.system_prompts import MEDICINE_SAFETY_PROMPT

def check_medicine_safety(medicines: list) -> dict:
    """Analyze medicines for interactions and timing guidance"""
    
    prompt = MEDICINE_SAFETY_PROMPT.format(medicines=json.dumps(medicines, indent=2))
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

def save_medicines(medicine_data: dict, filepath: str = "data/medicines.json"):
    """Save medicine analysis to JSON storage"""
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(medicine_data, f, indent=2)
    
    return medicine_data

def load_medicines(filepath: str = "data/medicines.json") -> dict:
    """Load saved medicines"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return {"medicines": []}
