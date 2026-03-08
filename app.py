from fastapi import FastAPI, UploadFile, File, Form
from backened.parser import extract_text
from backened.analyzer import analyze_resume
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(resume: UploadFile = File(...), job_description: str = Form(...)):

    resume_text = extract_text(resume.file)

    result = analyze_resume(resume_text, job_description)

    return result