import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

SKILL_SYNONYMS = {
    'python': ['python', 'python3'],
    'sql': ['sql', 'mysql', 'postgresql', 'nosql', 'mongodb'],
    'jira': ['jira', 'atlassian jira'],
    'postman': ['postman'],
    'selenium': ['selenium', 'selenium webdriver'],
    'api testing': ['api testing', 'rest api testing', 'restful api testing'],
    'manual testing': ['manual testing', 'functional testing', 'regression testing', 'black box testing', 'black-box testing', 'exploratory testing'],
    'automation testing': ['automation testing', 'test automation', 'automated testing'],
    'project management': ['project management', 'project coordination', 'stakeholder communication', 'requirement gathering', 'requirements gathering', 'scrum', 'agile'],
    'git': ['git', 'github', 'gitlab', 'bitbucket'],
    'java': ['java', 'j2ee'],
    'c++': ['c++', 'cpp'],
    'c#': ['c#', 'c-sharp'],
    'javascript': ['javascript', 'js', 'es6'],
    'react': ['react', 'reactjs', 'react.js'],
    'node.js': ['node.js', 'node js', 'nodejs'],
    'aws': ['aws', 'amazon web services'],
    'docker': ['docker', 'containerization'],
    'kubernetes': ['kubernetes', 'k8s'],
    'machine learning': ['machine learning', 'ml'],
    'nlp': ['nlp', 'natural language processing'],
    'qa': ['qa', 'quality assurance', 'software testing', 'test cases', 'test plans', 'uat', 'user acceptance testing'],
    'cicd': ['ci/cd', 'cicd', 'continuous integration', 'continuous deployment', 'jenkins'],
    'linux': ['linux', 'bash', 'shell scripting', 'unix']
}

def get_base_skills():
    return list(SKILL_SYNONYMS.keys())

def extract_keywords_new(text):
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    stop_words = set(ENGLISH_STOP_WORDS).union({
        'experience', 'years', 'work', 'job', 'role', 'team', 'company', 'skills', 
        'requirements', 'responsibilities', 'looking', 'candidate', 'strong', 'good',
        'ability', 'knowledge', 'understanding', 'working', 'using', 'design', 'development',
        'testing', 'build', 'create', 'maintain', 'support', 'ensure', 'help', 'required',
        'preferred', 'must', 'have', 'including', 'related', 'environment', 'business'
    })
    keywords = set([w for w in words if w not in stop_words])
    return keywords

def extract_skills_robust(text):
    text_lower = text.lower()
    found_skills = set()
    
    for standard_skill, synonyms in SKILL_SYNONYMS.items():
        for syn in synonyms:
            escaped_syn = re.escape(syn)
            # More robust word boundary that works even with non-alphanumeric chars
            start_bound = r'\b' if syn[0].isalnum() else r'(?:\s|^|[^\w])'
            end_bound = r'\b' if syn[-1].isalnum() else r'(?:\s|$|[^\w])'
            pattern = start_bound + escaped_syn + end_bound
            
            if re.search(pattern, text_lower):
                found_skills.add(standard_skill)
                break
                
    # Also add standard keyword searching as a fallback for missing dict entries
    fallback_skills = ['html', 'css', 'pytest', 'junit', 'rest api', 'graphql', 'azure', 'gcp', 'data structures', 'algorithms', 'frontend', 'backend', 'fullstack']
    for skill in fallback_skills:
        escaped_syn = re.escape(skill)
        start_bound = r'\b' if skill[0].isalnum() else r'(?:\s|^|[^\w])'
        end_bound = r'\b' if skill[-1].isalnum() else r'(?:\s|$|[^\w])'
        pattern = start_bound + escaped_syn + end_bound
        if re.search(pattern, text_lower):
            found_skills.add(skill)
            
    return found_skills

def extract_education(text):
    education_keywords = ['bachelor', 'master', 'phd', 'b.tech', 'm.tech', 'bsc', 'msc', 'degree', 'university', 'college', 'institute', 'diploma']
    return any(kw in text.lower() for kw in education_keywords)

def extract_experience(text):
    experience_keywords = ['experience', 'work history', 'employment', 'internship', 'years', 'role', 'developer', 'engineer', 'manager', 'coordinator', 'tester', 'analyst', 'qa', 'responsibilities', 'project']
    has_exp_kw = any(kw in text.lower() for kw in experience_keywords)
    has_years = bool(re.search(r'\d+\+?\s*(years?|yrs)', text.lower()))
    return has_exp_kw or has_years

def analyze_ats(resume_text, jd_text):
    if not resume_text or not jd_text:
        return None

    # 1. Keyword Match (40%)
    jd_keywords = extract_keywords_new(jd_text)
    resume_keywords = extract_keywords_new(resume_text)
    
    if not jd_keywords:
        keyword_score = 100
        matched_keywords = set()
    else:
        matched_keywords = jd_keywords.intersection(resume_keywords)
        keyword_score = (len(matched_keywords) / len(jd_keywords)) * 100
        
    # 2. Skills Match (30%)
    jd_skills = extract_skills_robust(jd_text)
    resume_skills = extract_skills_robust(resume_text)
    
    if not jd_skills:
        skill_score = 100
        matched_skills = set()
        missing_skills = set()
    else:
        matched_skills = jd_skills.intersection(resume_skills)
        missing_skills = jd_skills - resume_skills
        skill_score = (len(matched_skills) / len(jd_skills)) * 100
        
    # 3. Experience Match (20%)
    has_jd_exp = extract_experience(jd_text)
    has_resume_exp = extract_experience(resume_text)
    
    if not has_jd_exp:
        exp_score = 100 
    elif has_resume_exp:
        exp_score = 100
    else:
        exp_score = 0
        
    # 4. Education Match (10%)
    has_jd_edu = extract_education(jd_text)
    has_resume_edu = extract_education(resume_text)
    
    if not has_jd_edu:
        edu_score = 100
    elif has_resume_edu:
        edu_score = 100
    else:
        edu_score = 0
        
    # Calculate Final Weighted Score
    final_score = (keyword_score * 0.40) + (skill_score * 0.30) + (exp_score * 0.20) + (edu_score * 0.10)
    
    # Normalization & Category
    final_score = min(max(final_score, 0), 100)
    
    if final_score >= 90:
        category = "Excellent Match"
    elif final_score >= 75:
        category = "Good Match"
    elif final_score >= 60:
        category = "Moderate Match"
    else:
        category = "Needs Improvement"
        
    return {
        "final_score": round(final_score, 2),
        "category": category,
        "breakdown": {
            "keyword_score": round(keyword_score, 2),
            "skill_score": round(skill_score, 2),
            "exp_score": exp_score,
            "edu_score": edu_score
        },
        "skills": {
            "jd_skills": list(jd_skills),
            "resume_skills": list(resume_skills),
            "found": list(matched_skills),
            "missing": list(missing_skills)
        },
        "keywords": {
            "jd_keywords": list(jd_keywords),
            "resume_keywords": list(resume_keywords),
            "matched_keywords": list(matched_keywords),
            "missing_keywords": list(jd_keywords - resume_keywords)
        }
    }

def extract_contact_info(text):
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    phone = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    return {
        "email": email.group(0) if email else "Not Found",
        "phone": phone.group(0) if phone else "Not Found"
    }
