"""
Skill Extraction Prompt Template
"""

from langchain_core.prompts import PromptTemplate

# Skill Extraction Prompt
skill_extraction_template = """You are an expert HR recruiter with deep knowledge of technical skills and job requirements.

Extract all technical and professional skills from the following resume. 

IMPORTANT RULES:
- Only extract skills that are EXPLICITLY mentioned in the resume
- Do NOT assume or hallucinate skills not present
- Include: programming languages, tools, frameworks, soft skills, certifications
- Return structured JSON format

Resume:
{resume}

Return JSON with this exact structure:
{{
    "technical_skills": ["skill1", "skill2"],
    "tools_frameworks": ["tool1", "tool2"],
    "soft_skills": ["skill1", "skill2"],
    "experience_years": 0,
    "certifications": ["cert1"]
}}

JSON Output:"""

skill_extraction_prompt = PromptTemplate(
    input_variables=["resume"],
    template=skill_extraction_template
)
