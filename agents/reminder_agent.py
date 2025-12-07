"""Reminder Agent - Creates medication reminders with fallback"""
import json
from tools.gemini_client import generate_content
from prompts.system_prompts import REMINDER_PROMPT

def create_reminders(medicines: list) -> dict:
    """Create reminder schedule from medicine list"""
    
    prompt = REMINDER_PROMPT.format(schedule=json.dumps(medicines, indent=2))
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

def save_reminders(reminder_data: dict, filepath: str = "data/reminders.json"):
    """Save reminders to JSON storage"""
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(reminder_data, f, indent=2)
    
    return reminder_data
