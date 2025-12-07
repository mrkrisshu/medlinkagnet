"""Timeline Agent - Builds health journey timeline with fallback"""
import json
from tools.gemini_client import generate_content
from prompts.system_prompts import TIMELINE_PROMPT

def build_timeline(records: list) -> dict:
    """Build health timeline from accumulated records"""
    
    prompt = TIMELINE_PROMPT.format(records=json.dumps(records, indent=2))
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

def save_timeline(timeline_data: dict, filepath: str = "data/timeline.json"):
    """Save timeline to JSON storage"""
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(timeline_data, f, indent=2)
    
    return timeline_data

def load_timeline(filepath: str = "data/timeline.json") -> dict:
    """Load saved timeline"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return {"timeline": []}

def load_all_reports(filepath: str = "data/reports.json") -> list:
    """Load all saved reports for timeline building"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return []
