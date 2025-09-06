import os
from openai import OpenAI
from dotenv import load_dotenv
from medlineplus_service import get_medlineplus_topic
import requests

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(question, retrieved_chunks, patient_name=None, patient_age=None):
    # Query MedlinePlus for additional context
    medline_result = get_medlineplus_topic(question)
    medline_context = ""
    if medline_result:
        if medline_result.get("summary"):
            medline_context += f"MedlinePlus Summary:\n{medline_result['summary']}\n"
        if medline_result.get("url"):
            try:
                page_response = requests.get(medline_result["url"], timeout=10)
                page_response.raise_for_status()
                page_text = page_response.text
                # Use GPT to summarize the page
                medline_gpt_summary = generate_summary(page_text)
                medline_context += f"MedlinePlus Page Summary:\n{medline_gpt_summary}\n"
            except Exception as e:
                medline_context += f"Could not fetch MedlinePlus page: {str(e)}\n"

    # Combine all context
    context = "\n".join([doc for doc in retrieved_chunks])
    full_context = f"{context}\n{medline_context}"

    # Tailored prompt for the patient
    patient_info = ""
    if patient_name:
        patient_info += f"Patient Name: {patient_name}\n"
    if patient_age:
        patient_info += f"Patient Age: {patient_age}\n"

    prompt = f"""
    You are a highly knowledgeable and empathetic medical assistant. 
    Use the following context, including trusted medical sources like MedlinePlus, to answer the patient's question.
    Always tailor your response to the patient's details and needs.

    {patient_info}
    Context:
    {full_context}

    Patient's Question:
    {question}

    Please provide a clear, accurate, and patient-friendly answer, referencing MedlinePlus and other sources as appropriate.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or gpt-4o
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def generate_summary(text):
    prompt = f"""
    Summarize the following medical information in a concise, patient-friendly manner:
    {text}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or gpt-4o
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
