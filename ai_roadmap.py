import os
from groq import Groq
from dotenv import load_dotenv

# Load .env
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in .env")

client = Groq(api_key=api_key)

def generate_ai_roadmap(profile):

    try:
        prompt = f"""
        Student Profile:
        Projects: {profile['projects']}
        Internships: {profile['internships']}
        CGPA: {profile['cgpa']}
        Skills: {profile['skills']}
        Target Role: {profile['target_role']}

        Generate a structured 3-month roadmap in bullet points.
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # ✅ UPDATED MODEL
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ AI Error: {str(e)}"