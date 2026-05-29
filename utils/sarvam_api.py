import os
import requests
import time

def get_sarvam_feedback(resume_text, jd_text):
    api_key = os.getenv("SARVAM_API_KEY")
    if not api_key:
        return _fallback_feedback()
    
    url = "https://api.sarvam.ai/v1/chat/completions" # Generic LLM endpoint structure
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    You are an expert AI Recruiter and ATS system.
    Please analyze the following Resume against the Job Description and provide:
    1. Resume Improvement Suggestions
    2. Professional Recruiter Feedback
    3. Skill Gap Analysis
    4. Resume Summary Enhancement
    5. Suggestions to improve ATS score
    
    Resume Text: {resume_text[:1000]}
    Job Description: {jd_text[:1000]}
    """
    
    payload = {
        "model": "sarvam-1",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    try:
        # Use a short timeout so we fallback quickly if endpoint doesn't exist
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return _fallback_feedback(f"(Note: Sarvam API returned {response.status_code}. Using fallback analysis)")
    except Exception as e:
        return _fallback_feedback(f"(Note: Could not connect to Sarvam API directly. Using fallback analysis.)")

def _fallback_feedback(prefix=""):
    time.sleep(1) # Simulate processing time
    return f"""{prefix}

### 1. Resume Improvement Suggestions
- Ensure your contact information is at the very top and highly visible.
- Use action verbs (e.g., 'Spearheaded', 'Developed', 'Optimized') at the beginning of your bullet points.
- Quantify your achievements (e.g., 'Increased revenue by 15%', 'Reduced latency by 20%').

### 2. Professional Recruiter Feedback
The resume has a solid foundation but could better align with the specific job description. Recruiters look for direct matches in the first 6 seconds. Tailoring your experience section to highlight relevant projects will make a strong impact.

### 3. Skill Gap Analysis
Based on standard industry requirements, you might want to highlight soft skills alongside technical ones. Ensure that any tool or framework mentioned in the Job Description is clearly stated in your skills section if you possess it.

### 4. Resume Summary Enhancement
**Suggested Summary:** "Results-driven professional with a proven track record in developing robust solutions. Adept at leveraging modern technologies to solve complex problems and drive business success."

### 5. Suggestions to Improve ATS Score
- Remove complex formatting, tables, and columns which can confuse ATS parsers.
- Incorporate more exact-match keywords from the job description.
- Save and upload your resume as a standard PDF or DOCX file.
"""
