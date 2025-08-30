import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(question, retrieved_chunks):
    # Combine retrieved text
    context = "\n".join([doc for doc in retrieved_chunks])
    prompt = f"""
    You are a helpful medical assistant. Use the following context to answer the question.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or gpt-4o
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def generate_summary(text):
    prompt = f"""
    Summarize the following medical information in a concise manner:
    {text}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or gpt-4o
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content