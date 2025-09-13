import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from phi.storage.agent.sqlite import SqlAgentStorage

load_dotenv()

gemini_model = Gemini(id="gemini-2.5-flash")

resume_parser = Agent(
    name="Resume Parser",
    role="Extract skills, experience, internships, projects from PDF resumes",
    model=gemini_model,
    instructions=[
        "Parse the resume_text and extract structured data.",
        "Identify: skills, work experience, internships, projects.",
        "Return JSON format like: {'skills': [], 'experience': [], 'internships': [], 'projects': [] }"
    ],

    markdown=True,
)

job_recommender = Agent(
    name="Job Recommender",
    role="Recommend relevant jobs based on parsed resume data",
    model=gemini_model,
    tools=[DuckDuckGo()],
    instructions=[
        "Analyze skills and experience.",
        "Recommend 5 highly relevant and specific job roles.",
        "Respond with job titles for each. Use markdown bullet points.",
        "Avoid general answers. Base it only on input skills and roles."
    ],
    markdown=True,
)

career_coach = Agent(
    name="Career Coach",
    role="Provide personalized career guidance based on user's interest",
    model=gemini_model,
    tools=[DuckDuckGo()],
    instructions=[
        "Take the user's interested domain and suggest career advice.",
        "Recommend relevant certifications, skill growth plans, or roadmap.",
        "Return markdown structured advice with bullet points."
    ],
    markdown=True,
)

career_assistant_team = Agent(
    name="Career Assistant Team",
    model=gemini_model, 
    team=[resume_parser, job_recommender, career_coach],
    instructions=[
        "Step 1: Extract structured resume data",
        "Step 2: Recommend jobs based on the parsed data",
        "Step 3: Ask the user for their domain of interest, then provide career guidance"
    ],
    markdown=True,
)