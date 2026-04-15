"""
Explanation Prompt Template
"""

from langchain_core.prompts import PromptTemplate

# Explanation/Reasoning Prompt
explanation_template = """You are an expert HR recruiter explaining evaluation results to hiring managers.

Provide a clear, professional explanation of why this candidate received their score.

Candidate Skills:
{candidate_skills}

Matching Analysis:
{matching_analysis}

Fit Score:
{fit_score}

Job Context:
{job_requirements}

IMPORTANT RULES:
- Be balanced but honest about strengths and weaknesses
- Highlight critical missing requirements
- Suggest if this candidate should be considered for other roles
- Keep explanation concise (2-3 paragraphs)

Return JSON:
{{
    "summary": "brief summary",
    "strengths": "candidate strengths relevant to role",
    "weaknesses": "candidate gaps and concerns",
    "recommendation": "STRONG PASS/PASS/CONSIDER/REJECT",
    "next_steps": "suggested action"
}}

JSON Output:"""

explanation_prompt = PromptTemplate(
    input_variables=["candidate_skills", "matching_analysis", "fit_score", "job_requirements"],
    template=explanation_template
)
