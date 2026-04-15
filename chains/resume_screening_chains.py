"""
LangChain Chains for Resume Screening Pipeline
"""

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from prompts.skill_extraction_prompt import skill_extraction_prompt
from prompts.job_requirement_prompt import job_requirement_prompt
from prompts.matching_prompt import matching_prompt
from prompts.scoring_prompt import scoring_prompt
from prompts.explanation_prompt import explanation_prompt

# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

# JSON Parser
json_parser = JsonOutputParser()

# Step 1: Skill Extraction Chain
skill_extraction_chain = (
    skill_extraction_prompt 
    | llm 
    | json_parser
)

# Step 2: Job Requirement Extraction Chain
job_requirement_chain = (
    job_requirement_prompt 
    | llm 
    | json_parser
)

# Step 3: Matching Chain
matching_chain = (
    matching_prompt 
    | llm 
    | json_parser
)

# Step 4: Scoring Chain
scoring_chain = (
    scoring_prompt 
    | llm 
    | json_parser
)

# Step 5: Explanation Chain
explanation_chain = (
    explanation_prompt 
    | llm 
    | json_parser
)
