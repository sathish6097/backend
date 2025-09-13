from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
import tempfile
import traceback
from dotenv import load_dotenv
from pymongo import MongoClient
from main import analyze_resume  

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client["Sk"]
collection = db["resumes"]

app = FastAPI(title="Resume Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    userId: str
    fileUrl: str
    interests: str
    fullName: str
    education: str
    industries: str
    careerGoal: str

@app.get("/")
def root():
    return {"message": "Resume Analyzer is running!"}

@app.post("/analyze")
async def analyze_resume_by_user(data: AnalyzeRequest):
    try:
        print(f"📄 Downloading: {data.fileUrl}")
        response = requests.get(data.fileUrl)
        if response.status_code != 200:
            return JSONResponse(status_code=500, content={"error": "Resume file download failed"})

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(response.content)
            temp_pdf_path = tmp.name

     
        result = analyze_resume(
            pdf_resume_path=temp_pdf_path,
            user_interest=data.interests
        )

        if result is None:
            return JSONResponse(status_code=500, content={"error": "Resume analysis failed"})

        full_result = {
            "userId": data.userId,
            "fileUrl": data.fileUrl,
            "interests": data.interests,
            "fullName": data.fullName,
            "education": data.education,
            "industries": data.industries,
            "careerGoal": data.careerGoal,
            "analysisResult": result,
        }

        collection.update_one(
            {"userId": data.userId},
            {"$set": full_result},
            upsert=True
        )

        return JSONResponse(status_code=200, content=full_result)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
