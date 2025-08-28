from django.conf import settings
from langchain_groq import ChatGroq

def get_groq_api_key():
    return settings.GROQ_API_KEY

def get_groq_model(model="mixtral-8x7b-32768", **kwargs):
    if model is None:
        model = "llama-3.1-8b-instant"  # Fallback for compatibility

    return ChatGroq(
        model_name=model,
        temperature=0,  # Keep your deterministic setting
        max_tokens=2048,  # Explicit limit for free tier
        max_retries=2,  # Keep your retry logic
        api_key=get_groq_api_key(),
        **kwargs
    )