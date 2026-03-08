from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
import re

model = SentenceTransformer("all-MiniLM-L6-v2")


SKILLS_DB = [
"python","machine learning","ml","deep learning","nlp","flask","fastapi",
"sql","pandas","scikit-learn","tensorflow","pytorch","docker",
"aws","git","github","javascript","react","node","data analysis",
"rest api","api","kubernetes","cloud","linux"
]


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return text


def extract_skills(text):
    text = clean_text(text)
    skills = []

    for skill in SKILLS_DB:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            skills.append(skill)

    return skills


def skill_match(resume_skills, job_skills):
    if len(job_skills) == 0:
        return 0
    matched = len(set(resume_skills) & set(job_skills))
    return (matched / len(job_skills)) * 100


def keyword_overlap(resume_text, job_text):
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform([resume_text, job_text])
    similarity = (matrix * matrix.T).toarray()
    return similarity[0][1] * 100


def semantic_similarity(resume_text, job_text):
    emb1 = model.encode(resume_text)
    emb2 = model.encode(job_text)
    score = util.cos_sim(emb1, emb2)
    return float(score[0][0]) * 100


def rewrite_resume(resume_text, job_description):
    suggestions = []
    if "docker" in job_description:
        suggestions.append("Add Docker experience in your projects.")
    if "aws" in job_description:
        suggestions.append("Include AWS deployment or cloud experience.")
    if "tensorflow" in job_description:
        suggestions.append("Add TensorFlow or deep learning frameworks.")
    return suggestions


def analyze_resume(resume_text, job_description):

    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    skill_score = skill_match(resume_skills, job_skills)
    semantic_score = semantic_similarity(resume_text, job_description)
    keyword_score = keyword_overlap(resume_text, job_description)

    ats_score = (0.5 * skill_score) + (0.3 * semantic_score) + (0.2 * keyword_score)

    missing = list(set(job_skills) - set(resume_skills))
    suggestions = ai_feedback(resume_text, job_description)
    print("Resume Skills:", resume_skills)
    print("Job Skills:", job_skills)
    print("Missing Skills:", missing)

    return {
        "ATS Score": round(ats_score,2),
        "Skill Match %": round(skill_score,2),
        "Semantic Score": round(semantic_score,2),
        "Keyword Score": round(keyword_score,2),
        "Detected Skills": resume_skills,
        "Missing Skills": missing,
        "Suggestions": suggestions
    }
import requests

def ai_feedback(resume_text, job_description):

    suggestions = []

    if "docker" in job_description and "docker" not in resume_text:
        suggestions.append("Add Docker experience for ML deployment.")

    if "aws" in job_description and "aws" not in resume_text:
        suggestions.append("Include AWS cloud deployment experience.")

    if "tensorflow" in job_description and "tensorflow" not in resume_text:
        suggestions.append("Add TensorFlow or deep learning frameworks.")

    if len(suggestions) == 0:
        suggestions.append("Add more technical skills relevant to the job.")
        suggestions.append("Include measurable achievements in projects.")
        suggestions.append("Improve resume formatting with clear sections.")

    return suggestions