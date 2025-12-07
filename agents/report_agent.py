"""Report Extraction Agent - Uses Gemini Vision with proper file type handling"""
import json
import base64
from tools.gemini_client import generate_content
from prompts.system_prompts import REPORT_EXTRACTION_PROMPT

def extract_report(image_path: str = None, image_bytes: bytes = None, file_type: str = None) -> dict:
    """Extract medical data from report image/PDF"""
    
    if image_bytes:
        image_data = base64.b64encode(image_bytes).decode('utf-8')
    elif image_path:
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
    else:
        return {"error": "No image provided"}
    
    # Determine mime type
    if file_type == "application/pdf":
        mime_type = "application/pdf"
    elif file_type and file_type.startswith("image/"):
        mime_type = file_type
    else:
        # Try to detect from bytes
        if image_bytes and image_bytes[:4] == b'%PDF':
            mime_type = "application/pdf"
        elif image_bytes and image_bytes[:8] == b'\x89PNG\r\n\x1a\n':
            mime_type = "image/png"
        elif image_bytes and image_bytes[:2] == b'\xff\xd8':
            mime_type = "image/jpeg"
        else:
            mime_type = "image/png"  # default
    
    image_content = {"inline_data": {"mime_type": mime_type, "data": image_data}}
    
    response, model_used = generate_content(REPORT_EXTRACTION_PROMPT, image_content)
    
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

def save_report(report_data: dict, filepath: str = "data/reports.json"):
    """Save extracted report to JSON storage"""
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    try:
        with open(filepath, 'r') as f:
            reports = json.load(f)
    except:
        reports = []
    
    reports.append(report_data)
    
    with open(filepath, 'w') as f:
        json.dump(reports, f, indent=2)
    
    return reports
