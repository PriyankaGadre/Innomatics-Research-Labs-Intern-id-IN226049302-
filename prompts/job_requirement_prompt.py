"""
Job Requirement Extraction Prompt Template
"""

from langchain_core.prompts import PromptTemplate

# Job Requirement Extraction Prompt
job_requirement_template = """You are an expert HR recruiter with deep knowledge of job requirements.

Extract all technical and professional requirements from the following job description.

IMPORTANT RULES:
- Only extract requirements that are EXPLICITLY mentioned
- Return structured JSON format
- Distinguish between required and nice-to-have skills

Job Description:
{job_description}

Return JSON with this exact structure:
{{
    "required_skills": ["skill1", "skill2"],
    "required_tools": ["tool1", "tool2"],
    "nice_to_have": ["skill1"],
    "experience_years_required": 0,
    "education_required": "Bachelor's/Master's/High School",
    "certifications_required": ["cert1"]
}}

JSON Output:"""

job_requirement_prompt = PromptTemplate(
    input_variables=["job_description"],
    template=job_requirement_template
)
