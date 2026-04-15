# QUICK REFERENCE GUIDE
## AI Resume Screening System

### 📋 Quick Setup (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file with your keys
# Copy content from .env.example
# Add: OPENAI_API_KEY, LANGCHAIN_API_KEY

# 3. Run notebook
jupyter notebook AI_Resume_Screening_System.ipynb

# 4. Execute all cells (Kernel → Restart & Run All)
```

---

### 🔑 Environment Variables

```
OPENAI_API_KEY=sk-...              # Get from https://platform.openai.com
LANGCHAIN_API_KEY=ls_...           # Get from https://smith.langchain.com
LANGCHAIN_TRACING_V2=true          # Must be true for tracing
LANGCHAIN_PROJECT=Resume_Screening_System
```

---

### 📊 Expected Outputs

#### Strong Candidate
- Fit Score: 80-95 ✓
- Recommendation: STRONG PASS
- Matched Skills: 8-10 required

#### Average Candidate
- Fit Score: 60-75 ✓
- Recommendation: PASS / CONSIDER
- Matched Skills: 5-7 required

#### Weak Candidate
- Fit Score: 20-40 ✓
- Recommendation: REJECT
- Matched Skills: 0-3 required

---

### 🐛 Debugging

**Problem**: Pipeline fails to run
```
Solution: 
1. Check OPENAI_API_KEY is set
2. Restart Jupyter kernel
3. Run pip install -r requirements.txt again
```

**Problem**: LangSmith traces not showing
```
Solution:
1. Verify LANGCHAIN_TRACING_V2=true
2. Check LANGCHAIN_API_KEY is correct
3. Refresh https://smith.langchain.com
4. Check project name: Resume_Screening_System
```

**Problem**: JSON parsing errors
```
Solution:
1. Check LLM response in LangSmith trace
2. Verify prompt formatting
3. Try with temperature=0.3 (more deterministic)
```

---

### 📁 Project Structure

```
AI_Resume_screener/
├── AI_Resume_Screening_System.ipynb    ← MAIN FILE
├── main.py                              ← Logic
├── requirements.txt                     ← Dependencies
├── README.md                            ← Documentation
├── SUBMISSION_GUIDE.md                  ← How to submit
├── IMPLEMENTATION_SUMMARY.md            ← Details
├── .env.example                         ← Environment template
├── .gitignore                           ← Hide secrets
├── prompts/
│   ├── skill_extraction_prompt.py
│   ├── job_requirement_prompt.py
│   ├── matching_prompt.py
│   ├── scoring_prompt.py
│   └── explanation_prompt.py
├── chains/
│   └── resume_screening_chains.py
└── data/
    ├── sample_resumes.py
    └── job_description.py
```

---

### 🔗 Important Links

| Link | Purpose |
|------|---------|
| https://smith.langchain.com | View LangSmith traces |
| https://python.langchain.com/docs | LangChain documentation |
| https://platform.openai.com/api-keys | Get OpenAI API key |
| https://github.com/new | Create GitHub repo |
| https://linkedin.com | Post about your project |

---

### ✅ Submission Checklist

- [ ] All code completed and tested
- [ ] `.env` file configured with API keys
- [ ] Notebook runs without errors
- [ ] 3 test cases produce expected scores
- [ ] 3+ LangSmith traces visible
- [ ] GitHub repository created (PUBLIC)
- [ ] GitHub link is HTTPS format
- [ ] LinkedInpost created and published
- [ ] Both links ready for Google Form
- [ ] README.md and SUBMISSION_GUIDE.md included

---

### 🎯 Key Points

✓ **5-Step Pipeline**: Extract → Match → Score → Explain → Trace
✓ **LangChain**: Uses LCEL chains with .invoke() method
✓ **Anti-Hallucination**: Only explicit skills extracted
✓ **Tracing**: Full LangSmith visibility enabled
✓ **Testing**: 3 candidates with varied results
✓ **Documentation**: Comprehensive guides included

---

### 💡 Tips for Best Results

1. **Run full notebook** - All cells must execute
2. **Check LangSmith traces** - They prove tracing works
3. **Review outputs** - Verify realistic scores
4. **Polish code** - Clean, commented, professional
5. **Test on 3 candidates** - Strong, average, weak
6. **Create quality LinkedIn post** - Engaging content
7. **GitHub repository clean** - No API keys exposed
8. **Submit early** - Don't wait until deadline

---

### 📞 Need Help?

1. **Check README.md** - Most questions answered
2. **Review IMPLEMENTATION_SUMMARY.md** - Technical details
3. **View SUBMISSION_GUIDE.md** - Submission instructions
4. **Check LangSmith traces** - See what went wrong
5. **Read error messages** - Usually tell you the issue
6. **Ask on course forums** - Other students can help

---

### 🚀 Go-Live Checklist

Before final submission:
- [ ] Notebook is fully functional
- [ ] All required files present
- [ ] .env.example correctly formatted
- [ ] .gitignore protects secrets
- [ ] GitHub repository is public
- [ ] README.md is comprehensive
- [ ] LinkedIn post is published
- [ ] All links collected and verified

---

**Status**: Ready to execute and submit! 🎉
**Deadline**: April 16, 2026

Good luck! 👨‍💻
