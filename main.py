import time
import pdfplumber
from career_assistant import resume_parser, job_recommender, career_coach

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print("❌ Failed to extract text from PDF:", e)
        return None


def analyze_resume(pdf_resume_path: str, user_interest: str = "General"):
    resume_text = extract_text_from_pdf(pdf_resume_path)

    if not resume_text:
        print("❌ No resume text extracted.")
        return None

    try:
        print("\n--- STEP 1: Resume Parsing ---")
        parsed_output = resume_parser.run(f"Extract structured resume data:\n{resume_text}")
        parsed_data = parsed_output.content
        print(parsed_data)

        time.sleep(1)

        print("\n--- STEP 2: Job Recommendation ---")
        job_output = job_recommender.run(f"Based on this parsed data, recommend jobs:\n{parsed_data}")
        job_data = job_output.content
        print(job_data)

        time.sleep(1)

        print("\n--- STEP 3: Career Coaching Advice ---")
        advice_output = career_coach.run(
            f"The user is interested in {user_interest}. Provide career guidance."
        )
        advice_data = advice_output.content
        print(advice_data)

        return {
            "parsed_resume": parsed_data,
            "job_recommendations": job_data,
            "career_advice": advice_data,
        }

    except Exception as e:
        print("❌ Error during resume analysis:", e)
        return None
