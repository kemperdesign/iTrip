from typing import Optional, List, Dict, Any
from app.config import settings
from app.services.embeddings import search_similar
from openai import OpenAI
import anthropic
import google.generativeai as genai

openai_client = OpenAI(api_key=settings.openai_api_key)
anthropic_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)


def query_property_brain(
    question: str,
    document_id: Optional[int] = None,
    top_k: int = 5,
) -> Dict[str, Any]:
    """Answer a question using semantic search over documents."""

    # Search for relevant chunks
    search_results = search_similar(question, top_k=top_k, document_id=document_id)

    if not search_results:
        return {
            "answer": "No relevant information found in the documents.",
            "sources": [],
            "provider": settings.ai_provider,
        }

    # Format context from search results
    context = "\n\n".join([
        f"[From {result['document_id']} - Chunk {result['chunk_index']}]\n{result['text']}"
        for result in search_results
    ])

    # Build prompt
    system_prompt = """You are an AI assistant for a vacation rental property management company.
    You answer questions about properties, policies, and operations based on provided documents.
    Be concise, helpful, and always cite which document chunks you're referencing in your answer.
    If information is not found in the documents, say so clearly."""

    user_prompt = f"""Based on the following documents, answer this question: {question}

    Documents:
    {context}

    Provide a clear, concise answer citing the specific document chunks you're using."""

    # Get answer from configured AI provider
    answer = _get_ai_response(system_prompt, user_prompt)

    return {
        "answer": answer,
        "sources": [
            {
                "document_id": result["document_id"],
                "chunk_index": result["chunk_index"],
                "score": result["score"],
                "text_snippet": result["text"][:200] + "..." if len(result["text"]) > 200 else result["text"],
            }
            for result in search_results
        ],
        "provider": settings.ai_provider,
    }


def _get_ai_response(system_prompt: str, user_prompt: str) -> str:
    """Get response from configured AI provider."""

    if settings.ai_provider == "openai":
        return _openai_response(system_prompt, user_prompt)
    elif settings.ai_provider == "anthropic":
        return _anthropic_response(system_prompt, user_prompt)
    elif settings.ai_provider == "gemini":
        return _gemini_response(system_prompt, user_prompt)
    else:
        raise ValueError(f"Unknown AI provider: {settings.ai_provider}")


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

    # Combine system and user prompts for Gemini
    full_prompt = f"{system_prompt}\n\n{user_prompt}"
    response = model.generate_content(full_prompt)
    return response.text
