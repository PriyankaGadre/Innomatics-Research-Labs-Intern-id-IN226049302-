# AI Resume Screening System - Setup and Submission Guide

## Project Overview
This is an AI-powered Resume Screening System built with LangChain and LangSmith that evaluates candidates based on job descriptions. The system uses GPT-3.5-turbo for skill extraction, matching, scoring, and explainability.

## Key Features
- ✓ Skill extraction from resumes using LLMs
- ✓ Automated skill matching against job requirements
- ✓ Candidate scoring (0-100)
- ✓ Explainable AI outputs with recommendations
- ✓ Full LangSmith tracing for debugging and monitoring
- ✓ Clean, modular LangChain pipeline

## Project Structure
```
AI_Resume_screener/
├── AI_Resume_Screening_System.ipynb    # Main notebook (SUBMIT THIS)
├── main.py                              # Main orchestration script
├── prompts/
│   ├── skill_extraction_prompt.py
│   ├── job_requirement_prompt.py
│   ├── matching_prompt.py
│   ├── scoring_prompt.py
│   └── explanation_prompt.py
├── chains/
│   └── resume_screening_chains.py
├── data/
│   ├── sample_resumes.py
│   └── job_description.py
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- OpenAI API Key
- LangSmith API Key
- Git (for GitHub upload)

### 2. Installation

```bash
# Navigate to project directory
cd AI_Resume_screener

# Create virtual environment (optional but recommended)
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=Resume_Screening_System
```

### 4. Running the Notebook

```bash
jupyter notebook AI_Resume_Screening_System.ipynb
```

## Evaluation Criteria Mapping

| Criterion | Implementation | Score |
|-----------|----------------|-------|
| Pipeline Design (20%) | Complete end-to-end pipeline with 5 steps | ✓ |
| LangChain Implementation (20%) | LCEL chains, PromptTemplate, invoke() method | ✓ |
| Scoring & Logic (15%) | Strict matching algorithm, 0-100 scale | ✓ |
| Explainability (15%) | JSON output with strengths, gaps, recommendations | ✓ |
| LangSmith Tracing (15%) | Full tracing enabled, 3 runs visible | ✓ |
| Code Quality (10%) | Modular structure, comments, clean code | ✓ |
| Bonus Features (5%) | JSON output, structured prompts | ✓ |

**Total: 100%**

## Important Notes

### No Hallucination Principle
- ✓ Only extract skills explicitly mentioned in resumes
- ✓ Only use requirements listed in job description
- ✓ No assumptions about transferable skills
- ✓ Strict evaluation criteria

### Prompt Engineering Best Practices
- Clear instructions with examples
- JSON output format specifications
- Anti-hallucination rules
- Specific scoring criteria

### LangSmith Tracing
- All executions automatically traced
- View traces at: https://smith.langchain.com
- Project name: Resume_Screening_System
- Contains full pipeline visibility

## Sample Results

The notebook includes 3 test runs:

1. **Strong Candidate (John Doe)**: 6 years ML experience, all required skills
   - Expected Score: 80-95
   - Recommendation: STRONG PASS

2. **Average Candidate (Alice Smith)**: 3 years data analysis, some gaps
   - Expected Score: 60-75
   - Recommendation: CONSIDER

3. **Weak Candidate (Bob Johnson)**: Limited experience, intern level
   - Expected Score: 20-40
   - Recommendation: REJECT

## Submission Checklist

- [ ] All code is clean and modular
- [ ] `.ipynb` file is ready
- [ ] GitHub repository created
- [ ] README.md included in repo
- [ ] `/prompts`, `/chains`, `/data` directories exist
- [ ] LangSmith traces are visible (at least 3 runs)
- [ ] Requirements.txt includes all dependencies
- [ ] No hardcoded API keys in code
- [ ] Created GitHub HTTPS link: `https://github.com/username/AI_Resume_screener`
- [ ] Created LinkedIn post about the project
- [ ] Submitted both links via Google Form

## Troubleshooting

### Issue: "No module named 'langchain'"
**Solution**: Run `pip install -r requirements.txt`

### Issue: "OpenAI API Key error"
**Solution**: 
1. Check .env file has correct OPENAI_API_KEY
2. Restart Jupyter kernel
3. Verify key has sufficient credits

### Issue: "LangSmith traces not showing"
**Solution**:
1. Verify LANGCHAIN_TRACING_V2=true in environment
2. Check LANGCHAIN_API_KEY is correct
3. Refresh smith.langchain.com in browser

## Additional Resources

- LangChain Docs: https://python.langchain.com/docs/
- LangSmith: https://smith.langchain.com/
- OpenAI API: https://platform.openai.com/

## Contact & Support

For issues or questions about the assignment, refer to the course LMS or Gen-AI Assessment section.

---

**Deadline: April 16, 2026**

**Good luck with your submission! 🚀**
