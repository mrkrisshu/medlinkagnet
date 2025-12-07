"""Report Chat Agent - Conversational Q&A about uploaded reports"""
import json
from tools.gemini_client import generate_content

CHAT_PROMPT = """You are a helpful medical report assistant. The user has uploaded medical reports and wants to chat about them.

SAFETY RULES:
❌ Do NOT diagnose diseases
❌ Do NOT prescribe treatments
❌ Do NOT make medical decisions
✅ Explain what the report shows in simple terms
✅ Answer questions about report values
✅ Suggest questions to ask their doctor
✅ Always recommend consulting a doctor

UPLOADED REPORTS:
{reports}

USER QUESTION: {question}

Respond conversationally in {language}. Be helpful, clear, and always remind them to consult their doctor for medical decisions. Keep response concise."""


def chat_about_reports(reports: list, question: str, language: str = "english") -> str:
    """Have a conversation about the user's reports"""
    
    # Format reports for context
    reports_text = json.dumps(reports, indent=2, ensure_ascii=False)
    
    prompt = CHAT_PROMPT.format(
        reports=reports_text,
        question=question,
        language=language
    )
    
    response, model_used = generate_content(prompt)
    
    return response.text
