import pandas as pd
from src.processor.cleaner import DataCleaner
from src.processor.skill_analyzer import SkillAnalyzer

# Mock scraped dataset
sample_data = pd.DataFrame([
    {
        "job_title": "Senior Python Developer",
        "company": "Acme Corp",
        "location": "Remote",
        "salary": "$120k - $150k",
        "skills": "Python, AWS, Docker"
    },
    {
        "job_title": "Data Scientist",
        "company": "TechCorp",
        "location": "Worldwide",
        "salary": "$110,000/yr",
        "skills": "Python, SQL, Machine Learning, Pandas"
    },
    {
        "job_title": "Senior Python Developer",
        "company": "Acme Corp",
        "location": "Remote",
        "salary": "$120k - $150k",
        "skills": "Python, AWS, Docker"
    }
])

# Run cleaner
cleaner = DataCleaner()
cleaned_df = cleaner.clean_jobs_data(sample_data)

# Run skill analyzer
analyzer = SkillAnalyzer()
results = analyzer.analyze_market_trends(cleaned_df)

print("\n--- TEST RESULTS ---")
print(f"Cleaned Row Count (Deduplicated): {len(cleaned_df)} (Original was {len(sample_data)})")
print(f"Top Skills Detected: {results['skill_counts']}")
print(f"Calculated Metrics: {results['metrics']}")