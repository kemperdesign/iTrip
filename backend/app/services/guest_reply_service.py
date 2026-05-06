from typing import Optional, List, Dict, Any
from app.config import settings
from app.services.embeddings import search_similar
from openai import OpenAI
import anthropic
import google.generativeai as genai
import re

openai_client = OpenAI(api_key=settings.openai_api_key)
anthropic_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

# Risk keywords for escalation detection
RISK_KEYWORDS = {
    "refund": {"category": "payment", "risk_level": "high"},
    "refund request": {"category": "payment", "risk_level": "high"},
    "money back": {"category": "payment", "risk_level": "high"},
    "charge": {"category": "payment", "risk_level": "medium"},
    "overcharge": {"category": "payment", "risk_level": "high"},
    "deposit": {"category": "payment", "risk_level": "medium"},
    "damage": {"category": "property", "risk_level": "high"},
    "damaged": {"category": "property", "risk_level": "high"},
    "broken": {"category": "property", "risk_level": "high"},
    "stain": {"category": "property", "risk_level": "medium"},
    "hole": {"category": "property", "risk_level": "high"},
    "water": {"category": "property", "risk_level": "medium"},
    "leak": {"category": "property", "risk_level": "high"},
    "wet": {"category": "property", "risk_level": "medium"},
    "complaint": {"category": "complaint", "risk_level": "medium"},
    "issue": {"category": "complaint", "risk_level": "low"},
    "problem": {"category": "complaint", "risk_level": "low"},
    "urgent": {"category": "complaint", "risk_level": "high"},
    "angry": {"category": "complaint", "risk_level": "high"},
    "frustrated": {"category": "complaint", "risk_level": "medium"},
    "unhappy": {"category": "complaint", "risk_level": "medium"},
    "unsatisfied": {"category": "complaint", "risk_level": "medium"},
    "cancel": {"category": "cancellation", "risk_level": "high"},
    "cancellation": {"category": "cancellation", "risk_level": "high"},
    "not coming": {"category": "cancellation", "risk_level": "high"},
}


def detect_escalation_risks(message_text: str) -> Dict[str, Any]:
    """Analyze message for escalation keywords and determine risk level."""
    text_lower = message_text.lower()
    flagged_keywords = []
    risk_scores = {"payment": 0, "property": 0, "complaint": 0, "cancellation": 0}

    # Find all matching keywords
    for keyword, info in RISK_KEYWORDS.items():
        if keyword in text_lower:
            # Find context for the keyword (20 chars before and after)
            idx = text_lower.find(keyword)
            start = max(0, idx - 20)
            end = min(len(text_lower), idx + len(keyword) + 20)
            excerpt = message_text[start:end].strip()

            flagged_keywords.append({
                "keyword": keyword,
                "risk_level": info["risk_level"],
                "message_excerpt": excerpt,
            })

            risk_scores[info["category"]] += 1

    # Determine overall risk level
    total_flags = sum(risk_scores.values())

    if total_flags == 0:
        overall_risk = "low"
    elif (risk_scores["payment"] > 0 and risk_scores["property"] > 0) or total_flags > 2:
        overall_risk = "escalate"
    elif risk_scores["payment"] > 0 or risk_scores["property"] > 1:
        overall_risk = "high"
    elif risk_scores["property"] > 0 or risk_scores["cancellation"] > 0:
        overall_risk = "high"
    elif risk_scores["complaint"] > 1 or (risk_scores["complaint"] > 0 and any(kw["risk_level"] == "high" for kw in flagged_keywords)):
        overall_risk = "medium"
    else:
        overall_risk = "low"

    return {
        "risk_level": overall_risk,
        "flagged_keywords": flagged_keywords,
        "has_risk": len(flagged_keywords) > 0,
    }


def generate_guest_reply(
    message_text: str,
    template_doc_id: Optional[int] = None,
    ai_provider: Optional[str] = None,
    include_templates: bool = True,
) -> Dict[str, Any]:
    """Generate an AI-drafted reply to a guest message with template context."""

    # Detect escalation risks
    risk_analysis = detect_escalation_risks(message_text)

    # Search for relevant templates if enabled
    source_templates = []
    template_context = ""

    if include_templates and template_doc_id:
        search_results = search_similar(message_text, top_k=5, document_id=template_doc_id)
        if search_results:
            source_templates = [
                {
                    "document_id": result["document_id"],
                    "chunk_index": result["chunk_index"],
                    "score": result["score"],
                    "text_snippet": result["text"][:150] + "..." if len(result["text"]) > 150 else result["text"],
                }
                for result in search_results
            ]

            template_context = "Here are some example responses to similar guest messages that you can use as reference for tone and style:\n\n"
            template_context += "\n\n".join([
                f"[Template {i+1}] {result['text']}"
                for i, result in enumerate(search_results[:3])
            ])

    # Build system prompt
    system_prompt = """You are a professional guest relations assistant for a vacation rental company.
Your role is to draft helpful, courteous, and professional responses to guest messages.
Be empathetic, clear, and concise. When addressing concerns, acknowledge the guest's issue and explain how you'll help.
Always maintain a friendly and professional tone. Never make promises about refunds or compensation without clear policy guidance.
If escalation keywords are detected, prioritize swift, empathetic responses that acknowledge the concern."""

    # Build user prompt
    user_prompt = f"""Draft a professional response to this guest message:

GUEST MESSAGE:
{message_text}

ESCALATION INDICATORS: {', '.join([kw['keyword'] for kw in risk_analysis['flagged_keywords']]) if risk_analysis['flagged_keywords'] else 'None'}
RISK LEVEL: {risk_analysis['risk_level'].upper()}

{template_context if template_context else ''}

Provide a draft response that:
1. Addresses the guest's concern directly
2. Is professional and empathetic
3. Matches the tone and style of the example templates (if provided)
4. Is concise (1-3 short paragraphs)

DRAFT RESPONSE:"""

    # Get response from configured AI provider
    reply_text = _get_ai_response(system_prompt, user_prompt, ai_provider)

    return {
        "reply_text": reply_text,
        "risk_flags": risk_analysis["flagged_keywords"],
        "source_templates": source_templates,
        "requires_review": risk_analysis["risk_level"] in ["high", "escalate"],
        "ai_provider": ai_provider or settings.ai_provider,
        "ai_model": settings.ai_model,
    }


def _get_ai_response(system_prompt: str, user_prompt: str, ai_provider: Optional[str] = None) -> str:
    """Get response from configured AI provider."""
    provider = ai_provider or settings.ai_provider

    if provider == "openai":
        return _openai_response(system_prompt, user_prompt)
    elif provider == "anthropic":
        return _anthropic_response(system_prompt, user_prompt)
    elif provider == "gemini":
        return _gemini_response(system_prompt, user_prompt)
    else:
        raise ValueError(f"Unknown AI provider: {provider}")


def _openai_response(system_prompt: str, user_prompt: str) -> str:
    """Get response from OpenAI API."""
    response = openai_client.chat.completions.create(
        model=settings.ai_model or "gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=1024,
    )
    return response.choices[0].message.content


def _anthropic_response(system_prompt: str, user_prompt: str) -> str:
    """Get response from Anthropic Claude API."""
    response = anthropic_client.messages.create(
        model=settings.ai_model or "claude-opus-4-7",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.content[0].text


def _gemini_response(system_prompt: str, user_prompt: str) -> str:
    """Get response from Google Gemini API."""
    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel(settings.ai_model or "gemini-1.5-flash")

    full_prompt = f"{system_prompt}\n\n{user_prompt}"
    response = model.generate_content(full_prompt)
    return response.text
