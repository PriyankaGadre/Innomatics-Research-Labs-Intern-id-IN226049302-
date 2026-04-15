"""
Scoring Prompt Template
"""

from langchain_core.prompts import PromptTemplate

# Scoring Prompt
scoring_template = """You are an expert HR recruiter scoring candidate fit for a role.

Based on the skill match analysis, assign a score from 0-100.

Matching Analysis:
{matching_analysis}

Job Requirements:
{job_requirements}

Scoring Criteria (0-100):
- 90-100: Exceeds all requirements, strong candidate
- 80-89: Meets all requirements, good fit
- 70-79: Meets most requirements with minor gaps
- 60-69: Meets some requirements but has important gaps
- Below 60: Does not meet core requirements

IMPORTANT RULES:
- Consider: matched required skills, missing required skills, experience level
- Critical gaps in required skills significantly reduce score
- Do NOT be lenient

Return JSON:
{{
    "fit_score": 0,
    "score_justification": "explanation"
}}

JSON Output:"""

scoring_prompt = PromptTemplate(
    input_variables=["matching_analysis", "job_requirements"],
    template=scoring_template
)
