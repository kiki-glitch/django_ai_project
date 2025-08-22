from django.conf import settings
from langchain_groq import ChatGroq

def get_groq_api_key():
    return settings.GROQ_API_KEY

def get_groq_model(model="llama3-8b-8192", **kwargs):
    if model is None:
        model = "llama3-8b-8192" 

    return ChatGroq(
        model_name=model,
        temperature=0,
        max_retries=2,
        api_key=get_groq_api_key(),  
        **kwargs
    )