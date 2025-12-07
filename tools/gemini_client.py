"""OpenRouter API client - Free models without rate limits"""
import os
import requests
import base64

# Try Streamlit secrets first (for cloud deployment), then env var
try:
    import streamlit as st
    OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY", ""))
except:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Working models on OpenRouter (verified names)
FREE_MODELS = [
    "google/gemini-2.0-flash-lite-001"
]

def generate_content(prompt: str, image_data: dict = None):
    """Generate content using OpenRouter free models"""
    
    messages = []
    
    if image_data:
        # Vision request with image
        content = [{"type": "text", "text": prompt}]
        if "inline_data" in image_data:
            img_base64 = image_data["inline_data"]["data"]
            mime_type = image_data["inline_data"].get("mime_type", "image/png")
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:{mime_type};base64,{img_base64}"}
            })
        messages = [{"role": "user", "content": content}]
    else:
        # Text-only request
        messages = [{"role": "user", "content": prompt}]
    
    last_error = None
    for model in FREE_MODELS:
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:8501",
                    "X-Title": "MedLink Agent"
                },
                json={
                    "model": model,
                    "messages": messages
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                text = result["choices"][0]["message"]["content"]
                
                # Create a simple response object
                class Response:
                    pass
                resp = Response()
                resp.text = text
                return resp, model
            else:
                last_error = f"Status {response.status_code}: {response.text}"
                continue
                
        except Exception as e:
            last_error = str(e)
            continue
    
    raise Exception(f"All models failed. Last error: {last_error}")
