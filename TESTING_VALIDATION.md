# TESTING & VALIDATION GUIDE
## Verify Your AI Resume Screening System Works Correctly

### Pre-Submission Validation Checklist

Before submitting, validate all components work as expected.

---

## ✅ Test 1: Environment Setup

### What to Verify
- Python version 3.9+
- All dependencies installed
- API keys configured
- LangSmith tracing enabled

### How to Test

**Test 1a: Python Version**
```bash
python --version
# Expected output: Python 3.9.x or higher
```

**Test 1b: Dependencies**
```bash
pip list | grep -E "langchain|openai|langsmith|jupyter"
# Should see:
# langchain-core
# langchain-openai
# langsmith
# jupyter
```

**Test 1c: Environment Variables**
```python
import os
print(f"OpenAI Key: {'✓' if 'OPENAI_API_KEY' in os.environ else '✗'}")
print(f"LangSmith Key: {'✓' if 'LANGCHAIN_API_KEY' in os.environ else '✗'}")
print(f"Tracing Enabled: {os.environ.get('LANGCHAIN_TRACING_V2', 'false')}")
```

**Expected Output**:
```
OpenAI Key: ✓
LangSmith Key: ✓
Tracing Enabled: true
```

---

## ✅ Test 2: Data Loading

### What to Verify
- Sample resumes load correctly
- Job description is accessible
- All data is properly formatted

### How to Test

```python
from data.sample_resumes import RESUMES, JOB_DESCRIPTION
from data.job_description import get_job_description

# Check resumes
print(f"Resumes loaded: {len(RESUMES)}")
for candidate_type, data in RESUMES.items():
    print(f"  {candidate_type}: {len(data['resume'])} characters")

# Check job description
job_desc = get_job_description()
print(f"Job description: {len(job_desc)} characters")
```

**Expected Output**:
```
Resumes loaded: 3
  strong: 2500+ characters
  average: 1500+ characters
  weak: 800+ characters
Job description: 3000+ characters
```

---

## ✅ Test 3: LangChain Chain Building

### What to Verify
- All prompt templates load
- All chains build without errors
- .invoke() method works

### How to Test

```python
from prompts.skill_extraction_prompt import skill_extraction_prompt
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser

# Initialize components
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
json_parser = JsonOutputParser()

# Build chain
skill_chain = skill_extraction_prompt | llm | json_parser

# Test with sample resume
test_resume = "Python developer with 5 years experience in TensorFlow and scikit-learn"
result = skill_chain.invoke({"resume": test_resume})

print("Chain Test Result:")
print(f"  Type: {type(result)}")
print(f"  Keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
```

**Expected Output**:
```
Chain Test Result:
  Type: <class 'dict'>
  Keys: dict_keys(['technical_skills', 'tools_frameworks', 'soft_skills', 'experience_years', 'certifications'])
```

---

## ✅ Test 4: Full Pipeline Execution

### What to Verify
- Complete pipeline runs without errors
- All 5 steps execute successfully
- Outputs are valid JSON

### How to Test

```python
from main import ResumeScreeningPipeline
from data.sample_resumes import STRONG_CANDIDATE_RESUME
from data.job_description import JOB_DESCRIPTION

# Create pipeline
pipeline = ResumeScreeningPipeline()

# Process job description
job_reqs = pipeline.process_job_description(JOB_DESCRIPTION)
print("✓ Job requirements extracted")

# Screen one candidate
result = pipeline.screen_resume(
    resume=STRONG_CANDIDATE_RESUME,
    candidate_name="Test Candidate",
    candidate_type="strong"
)

print("✓ Screening complete")

# Verify result structure
required_keys = ["skills_extracted", "matching_analysis", "scoring", "explanation"]
for key in required_keys:
    if key in result:
        print(f"  ✓ {key}")
    else:
        print(f"  ✗ {key} MISSING!")
```

**Expected Output**:
```
✓ Job requirements extracted
✓ Screening complete
  ✓ skills_extracted
  ✓ matching_analysis
  ✓ scoring
  ✓ explanation
```

---

## ✅ Test 5: Output Validation

### What to Verify
- Fit scores are in valid range (0-100)
- Recommendations are appropriate
- No hallucinated skills

### How to Test After Running Notebook

```python
import json

# Load results
with open("screening_results.json", "r") as f:
    results = json.load(f)

print("Output Validation Report")
print("=" * 60)

for i, result in enumerate(results, 1):
    print(f"\nCandidate {i}: {result['candidate_name']}")
    
    # Check scoring
    fit_score = result["scoring"].get("fit_score", -1)
    if 0 <= fit_score <= 100:
        print(f"  ✓ Fit Score: {fit_score}/100")
    else:
        print(f"  ✗ Invalid fit score: {fit_score}")
    
    # Check recommendation
    rec = result["explanation"].get("recommendation", "")
    valid_recs = ["STRONG PASS", "PASS", "CONSIDER", "REJECT"]
    if rec in valid_recs:
        print(f"  ✓ Recommendation: {rec}")
    else:
        print(f"  ✗ Invalid recommendation: {rec}")
    
    # Check JSON keys
    for key in ["skills_extracted", "matching_analysis", "scoring", "explanation"]:
        if key in result:
            print(f"  ✓ {key} present")
        else:
            print(f"  ✗ {key} MISSING")

print("\n" + "=" * 60)
```

**Expected Output**:
```
Output Validation Report
============================================================

Candidate 1: John Doe
  ✓ Fit Score: 85/100
  ✓ Recommendation: STRONG PASS
  ✓ skills_extracted present
  ✓ matching_analysis present
  ✓ scoring present
  ✓ explanation present

Candidate 2: Alice Smith
  ✓ Fit Score: 65/100
  ✓ Recommendation: CONSIDER
  ✓ skills_extracted present
  ✓ matching_analysis present
  ✓ scoring present
  ✓ explanation present

Candidate 3: Bob Johnson
  ✓ Fit Score: 28/100
  ✓ Recommendation: REJECT
  ✓ skills_extracted present
  ✓ matching_analysis present
  ✓ scoring present
  ✓ explanation present

============================================================
```

---

## ✅ Test 6: LangSmith Tracing Verification

### What to Verify
- Tracing is enabled
- Traces are visible in LangSmith
- All pipeline steps are captured

### How to Test

**Step 1: Programmatic Check**
```python
import os

print("LangSmith Tracing Configuration:")
print(f"  LANGCHAIN_TRACING_V2: {os.environ.get('LANGCHAIN_TRACING_V2', 'NOT SET')}")
print(f"  LANGCHAIN_PROJECT: {os.environ.get('LANGCHAIN_PROJECT', 'NOT SET')}")
print(f"  LANGCHAIN_API_KEY: {'SET' if 'LANGCHAIN_API_KEY' in os.environ else 'NOT SET'}")

if os.environ.get('LANGCHAIN_TRACING_V2').lower() == 'true':
    print("\n✓ Tracing is ENABLED")
else:
    print("\n✗ Tracing is DISABLED - FIX THIS!")
```

**Step 2: Web Dashboard Check**
1. Go to: https://smith.langchain.com
2. Login with your credentials
3. Look for project: `Resume_Screening_System`
4. Should see 3+ runs (one per candidate)
5. Each run should have 5 steps

**Check Each Trace**:
- Click on a run
- Verify you see:
  - Job Requirement Extraction
  - Skill Extraction
  - Skill Matching
  - Scoring
  - Explanation

---

## ✅ Test 7: Anti-Hallucination Validation

### What to Verify
- Only explicit skills are extracted
- No assumed skills
- Matches are accurate

### How to Manually Check

**Create a test resume:**
```
John Smith
Skills: Python, SQL

Nothing else - no mention of machine learning, deep learning, etc.
```

**Run through pipeline and verify:**
```python
test_resume = """
John Smith
Skills: Python, SQL

Nothing else - no mention of machine learning, deep learning, etc.
"""

result = skill_chain.invoke({"resume": test_resume})

# Should ONLY contain Python and SQL
print(result['technical_skills'])
# Expected: ['Python', 'SQL']
# NOT acceptable: ['Python', 'SQL', 'Machine Learning', 'Data Analysis', ...]
```

**Expected Result**:
```
['Python', 'SQL']  # ✓ CORRECT
```

**NOT Acceptable**:
```
['Python', 'SQL', 'Machine Learning', 'Statistics', ...]  # ✗ HALLUCINATING
```

---

## ✅ Test 8: Score Logic Validation

### What to Verify
- Strong candidate gets high score (80+)
- Average candidate gets medium score (60-75)
- Weak candidate gets low score (<60)

### Expected Results

| Candidate | Expected Range | Should Receive |
|-----------|-----------------|-----------------|
| Strong    | 80-95           | High (80+) |
| Average   | 60-75           | Medium (60-75) |
| Weak      | 20-50           | Low (<60) |

### How to Validate

After running the notebook:
```python
import json

with open("screening_results.json") as f:
    results = json.load(f)

print("Score Validation:")
for result in results:
    candidate_type = result["candidate_type"]
    score = result["scoring"]["fit_score"]
    
    if candidate_type == "strong":
        status = "✓ PASS" if score >= 80 else "✗ FAIL"
        print(f"  Strong Candidate: {score}/100 {status}")
    elif candidate_type == "average":
        status = "✓ PASS" if 60 <= score <= 75 else "✗ FAIL"
        print(f"  Average Candidate: {score}/100 {status}")
    elif candidate_type == "weak":
        status = "✓ PASS" if score < 60 else "✗ FAIL"
        print(f"  Weak Candidate: {score}/100 {status}")
```

**Expected Output**:
```
Score Validation:
  Strong Candidate: 85/100 ✓ PASS
  Average Candidate: 68/100 ✓ PASS
  Weak Candidate: 32/100 ✓ PASS
```

---

## ✅ Test 9: GitHub Repository Validation

### What to Verify
- Repository is created
- All files are present
- No sensitive files exposed
- Repository is public

### How to Test

```bash
# Navigate to GitHub repo URL in browser
https://github.com/YOUR_USERNAME/AI_Resume_screener

# Checklist:
# ✓ Repository page loads
# ✓ README.md displays in preview
# ✓ Files visible: main.py, requirements.txt, etc.
# ✓ .env file is NOT visible
# ✓ prompts/ folder visible
# ✓ chains/ folder visible
# ✓ data/ folder visible
# ✓ Repository says "Public"
```

**Command Line Check**:
```bash
cd AI_Resume_screener
git remote -v
# Should show:
# origin  https://github.com/YOUR_USERNAME/AI_Resume_screener.git (fetch)
# origin  https://github.com/YOUR_USERNAME/AI_Resume_screener.git (push)
```

---

## ✅ Test 10: Final Integration Test

### Complete End-to-End Validation

Run this comprehensive test:

```python
# FINAL INTEGRATION TEST
print("=" * 80)
print("FINAL INTEGRATION TEST - AI Resume Screening System")
print("=" * 80)

# 1. Environment
print("\n✓ Test 1: Environment")
import os
assert "OPENAI_API_KEY" in os.environ, "Missing OPENAI_API_KEY"
assert "LANGCHAIN_API_KEY" in os.environ, "Missing LANGCHAIN_API_KEY"
assert os.environ.get("LANGCHAIN_TRACING_V2") == "true", "Tracing not enabled"
print("  ✓ All environment variables set correctly")

# 2. Dependencies
print("\n✓ Test 2: Dependencies")
import langchain
import langchain_openai
import langsmith
import pandas
print("  ✓ All dependencies imported successfully")

# 3. Data
print("\n✓ Test 3: Data Loading")
from data.sample_resumes import RESUMES
from data.job_description import JOB_DESCRIPTION
assert len(RESUMES) == 3, "Should have 3 resumes"
assert len(JOB_DESCRIPTION) > 100, "Job description too short"
print("  ✓ All sample data loaded correctly")

# 4. Pipeline
print("\n✓ Test 4: Pipeline Creation")
from main import ResumeScreeningPipeline
pipeline = ResumeScreeningPipeline()
print("  ✓ Pipeline instance created")

# 5. Job Requirements
print("\n✓ Test 5: Job Requirements Processing")
job_reqs = pipeline.process_job_description(JOB_DESCRIPTION)
assert isinstance(job_reqs, dict), "Job requirements should be dict"
assert "required_skills" in job_reqs, "Missing required_skills"
print(f"  ✓ Extracted {len(job_reqs['required_skills'])} required skills")

# 6. Screening
print("\n✓ Test 6: Candidate Screening")
for candidate_type, data in RESUMES.items():
    result = pipeline.screen_resume(
        resume=data["resume"],
        candidate_name=data["name"],
        candidate_type=candidate_type
    )
    fit_score = result["scoring"]["fit_score"]
    assert 0 <= fit_score <= 100, f"Invalid score: {fit_score}"
    print(f"  ✓ {candidate_type.capitalize()}: {fit_score}/100")

# 7. Export
print("\n✓ Test 7: Results Export")
output_file = pipeline.export_results()
import json
with open(output_file) as f:
    exported = json.load(f)
    assert len(exported) == 3, "Should have 3 results"
print(f"  ✓ Results exported to {output_file}")

print("\n" + "=" * 80)
print("✅ ALL TESTS PASSED - READY FOR SUBMISSION")
print("=" * 80)
```

**Expected Output**:
```
================================================================================
FINAL INTEGRATION TEST - AI Resume Screening System
================================================================================

✓ Test 1: Environment
  ✓ All environment variables set correctly

✓ Test 2: Dependencies
  ✓ All dependencies imported successfully

✓ Test 3: Data Loading
  ✓ All sample data loaded correctly

✓ Test 4: Pipeline Creation
  ✓ Pipeline instance created

✓ Test 5: Job Requirements Processing
  ✓ Extracted 10 required skills

✓ Test 6: Candidate Screening
  ✓ Strong: 85/100
  ✓ Average: 68/100
  ✓ Weak: 32/100

✓ Test 7: Results Export
  ✓ Results exported to screening_results.json

================================================================================
✅ ALL TESTS PASSED - READY FOR SUBMISSION
================================================================================
```

---

## Test Results Summary

After completing all tests, you should have:

✅ Environment properly configured
✅ All dependencies installed
✅ Data loaded successfully
✅ Chains built correctly
✅ Full pipeline executes
✅ Valid output generated
✅ LangSmith traces visible
✅ No hallucinations detected
✅ Scores in expected ranges
✅ GitHub repo ready
✅ LinkedIn post published
✅ Google Form ready for submission

---

## If Tests Fail

### Common Issues & Fixes

**Test 1 Fails: Environment Variables Not Set**
```
Fix: Create .env file with correct keys
```

**Test 2 Fails: Dependencies Not Installed**
```
Fix: pip install -r requirements.txt
```

**Test 4 Fails: Pipeline Error**
```
Fix: Check API keys, restart Jupyter kernel
```

**Test 6 Fails: Scoring Logic Error**
```
Fix: Check LangSmith traces for LLM response issues
```

**Test 7 Fails: Export Error**
```
Fix: Ensure permissions to write screening_results.json
```

---

## Final Checklist

Before submitting, confirm ALL tests pass:

- [ ] Test 1: Environment Setup ✓
- [ ] Test 2: Data Loading ✓
- [ ] Test 3: LangChain Chain Building ✓
- [ ] Test 4: Full Pipeline Execution ✓
- [ ] Test 5: Output Validation ✓
- [ ] Test 6: LangSmith Tracing ✓
- [ ] Test 7: Anti-Hallucination ✓
- [ ] Test 8: Score Logic ✓
- [ ] Test 9: GitHub Repository ✓
- [ ] Test 10: Final Integration ✓

---

**WHEN ALL TESTS PASS → YOU'RE READY TO SUBMIT! 🚀**
