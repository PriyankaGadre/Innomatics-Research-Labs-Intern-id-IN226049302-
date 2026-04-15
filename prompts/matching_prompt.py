"""
Skill Matching Prompt Template
"""

from langchain_core.prompts import PromptTemplate

# Skill Matching Prompt
matching_template = """You are an expert HR recruiter evaluating candidate fit for a role.

Compare the candidate's skills with job requirements and identify matches and gaps.

Candidate Skills:
{candidate_skills}

Job Requirements:
{job_requirements}

IMPORTANT RULES:
- Only count exact or highly relevant matches
- Do NOT assume transferable skills
- Be strict in your evaluation
- Focus on required skills first

Analyze and return JSON:
{{
    "matched_required": ["skill1"],
    "missing_required": ["skill1"],
    "matched_nice_to_have": ["skill1"],
    "additional_strengths": ["skill1"],
    "critical_gaps": ["gap1"]
}}

JSON Output:"""

matching_prompt = PromptTemplate(
    input_variables=["candidate_skills", "job_requirements"],
    template=matching_template
)
