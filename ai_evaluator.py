import google.generativeai as genai
from groq import Groq
import json
import re

def configure_gemini(api_key):
    genai.configure(api_key=api_key)

def evaluate_candidates(resume_data, jd_text, provider="Gemini", model_name="gemini-1.5-flash", api_key=None):
    """
    Evaluates multiple candidates against a JD using the selected AI provider.
    resume_data is a list of dicts: [{"name": "...", "text": "..."}]
    Returns a JSON list of evaluations.
    """
    resume_block = "\n\n".join([f"Candidate Name: {r['name']}\nResume Text:\n{r['text']}" for r in resume_data])
    
    prompt = f"""You are an expert HR AI Resume Screener. Your task is to evaluate the following candidates against the provided Job Description.
    
Job Description:
{jd_text}

Candidates:
{resume_block}

For each candidate, provide:
1. match_score (0-100) based on Skills, Experience, and Fit.
2. strengths (list of length 2-3 strings)
3. gaps (list of length 2-3 strings)
4. recommendation (Strong Fit, Moderate Fit, or Not Fit)

Output the result EXACTLY as a JSON array of objects, with these exact keys: "name", "match_score", "strengths", "gaps", "recommendation".
Do not include markdown blocks like ```json around the response, just the raw JSON array.
"""

    text = ""
    if provider == "Gemini":
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        text = response.text.strip()
    elif provider == "Groq":
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        text = response.choices[0].message.content.strip()
    
    # Strip markdown if present
    text = re.sub(r'^```[a-zA-Z]*\n', '', text)
    text = re.sub(r'\n```$', '', text)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Fallback if parsing fails
        print("Failed to parse JSON. Raw output:", text)
        return []
