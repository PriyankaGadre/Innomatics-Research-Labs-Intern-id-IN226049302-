"""
Sample Resumes - Strong, Average, and Weak Candidates
"""

# Strong Candidate Resume
STRONG_CANDIDATE_RESUME = """
JOHN DOE
john.doe@email.com | (123) 456-7890 | LinkedIn: linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Data Scientist with 6 years of experience in machine learning, statistical analysis, and Python development. 
Proven track record of building and deploying predictive models in production environments.

EXPERIENCE

Senior Data Scientist | Tech Company Inc. | Jan 2022 - Present
- Developed and deployed 15+ machine learning models using Python, scikit-learn, and TensorFlow
- Led data pipeline optimization reducing processing time by 40%
- Implemented A/B testing framework using statistical analysis
- Mentored junior data scientists and conducted code reviews
- Used AWS (S3, EC2, SageMaker) for scalable infrastructure

Data Scientist | Analytics Corp | Jun 2020 - Dec 2021
- Built predictive models for customer churn (XGBoost, Random Forest) with 85% accuracy
- Created data visualizations using Tableau and Matplotlib
- Conducted SQL queries from PostgreSQL and MySQL databases
- Collaborated with product teams using Agile/Scrum methodology
- Implemented CI/CD pipelines using Git and Jenkins

Machine Learning Engineer | StartUp AI | Jan 2019 - May 2020
- Developed NLP models for text classification using NLTK and spaCy
- Built REST APIs using Flask for model deployment
- Implemented Docker containerization for application deployment
- Used Jupyter Notebook for exploratory data analysis

EDUCATION
M.S. in Data Science | University of Data | 2019
B.S. in Statistics | College of Science | 2017

TECHNICAL SKILLS
Programming Languages: Python, R, SQL, Java
ML Frameworks: TensorFlow, scikit-learn, PyTorch, XGBoost
Data Tools: Pandas, NumPy, Matplotlib, Seaborn, Plotly
Databases: PostgreSQL, MySQL, MongoDB, Redis
Cloud Platforms: AWS (S3, EC2, SageMaker), Google Cloud Platform
Other Tools: Git, Docker, Jupyter Notebook, Apache Spark, Tableau
Statistical Methods: Regression, Classification, Clustering, Time Series Analysis

CERTIFICATIONS
AWS Certified Machine Learning Specialty (2021)
Google Cloud Professional Data Engineer (2020)

PROJECTS
- Built end-to-end recommendation system using collaborative filtering (Python, Flask, PostgreSQL)
- Developed real-time sentiment analysis system for social media data (NLTK, Spark)
"""

# Average Candidate Resume
AVERAGE_CANDIDATE_RESUME = """
ALICE SMITH
alice.smith@email.com | (234) 567-8901 | LinkedIn: linkedin.com/in/alicesmith

PROFESSIONAL SUMMARY
Data Analyst with 3 years of experience in data analysis, reporting, and basic statistical analysis. 
Comfortable with Python and SQL for data manipulation and visualization.

EXPERIENCE

Data Analyst | Software Solutions Ltd. | Jul 2022 - Present
- Analyzed business data using SQL queries from a Postgres database
- Created Excel dashboards and Power BI reports for stakeholders
- Performed basic statistical analysis and reporting
- Used Python (Pandas, NumPy) for data cleaning and analysis
- Collaborated with product teams on ad-hoc data requests

Junior Data Analyst | Marketing Agency | Feb 2021 - Jun 2022
- Extracted data from company databases using SQL
- Created charts and visualizations using Excel and Google Sheets
- Assisted in A/B testing analysis and reporting
- Basic Python scripting for data processing

Data Entry Specialist | Retail Corp | Jan 2020 - Jan 2021
- Entered and verified data in company systems
- Created basic reports in Excel

EDUCATION
B.S. in Business Administration | State University | 2020

TECHNICAL SKILLS
Programming: Python (pandas, NumPy basics), SQL
Tools: Excel, Power BI, Google Sheets
Databases: PostgreSQL, MySQL
Other: Git (basic), Jupyter Notebook (basic)
Statistical Knowledge: Descriptive statistics, basic A/B testing

PROJECTS
- Analyzed customer purchase data using pandas (personal project)
- Created sales dashboard in Power BI
"""

# Weak Candidate Resume
WEAK_CANDIDATE_RESUME = """
BOB JOHNSON
bob@email.com | (345) 678-9012

PROFESSIONAL SUMMARY
Enthusiastic professional interested in data science and analytics. Strong communication skills.

EXPERIENCE

Data Team Intern | Tech Company | Summer 2023
- Helped organize and sort datasets
- Assisted with Excel spreadsheet creation
- Attended data team meetings

Retail Associate | Store Inc. | 2022 - 2023
- Customer service and sales support

Office Administrator | Small Business | 2021 - 2022
- Administrative tasks and filing

EDUCATION
High School Diploma | Local High School | 2021

SKILLS
- Excel (basic)
- Microsoft Office
- Customer Service
- Strong work ethic
- Quick learner

LANGUAGES
- English (native)
- Spanish (conversational)
"""

# Store resumes in dictionary for easy access
RESUMES = {
    "strong": STRONG_CANDIDATE_RESUME,
    "average": AVERAGE_CANDIDATE_RESUME,
    "weak": WEAK_CANDIDATE_RESUME,
}
