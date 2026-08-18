import re
import pandas as pd
from collections import Counter
from typing import List, Dict

# High-demand tech vocabulary to track
TARGET_SKILLS = [
    "Python", "SQL", "JavaScript", "TypeScript", "React", "Node.js", "AWS", "Docker",
    "Kubernetes", "Git", "FastAPI", "Django", "GraphQL", "PostgreSQL", "MongoDB",
    "Machine Learning", "Data Analysis", "Pytorch", "TensorFlow", "Pandas", "Scikit-Learn",
    "GCP", "Azure", "CI/CD", "Tailwind", "Java", "C++", "Go", "Rust"
]

class SkillAnalyzer:
    def __init__(self, target_skills: List[str] = TARGET_SKILLS):
        self.target_skills = target_skills
        self.skill_lookup = {skill.lower(): skill for skill in target_skills}

    def extract_skills_from_text(self, text: str) -> List[str]:
        """Identifies tech skills from descriptions or tag strings."""
        if not text or pd.isna(text):
            return []
        
        found = set()
        clean_text = re.sub(r"[^a-zA-Z0-9\+\#\.\s]", " ", str(text).lower())
        tokens = set(clean_text.split())
        
        for skill_lower, skill_original in self.skill_lookup.items():
            if " " in skill_lower:
                if skill_lower in clean_text:
                    found.add(skill_original)
            else:
                if skill_lower in tokens:
                    found.add(skill_original)
                    
        return sorted(list(found))

    def analyze_market_trends(self, df: pd.DataFrame) -> Dict:
        """Computes top skill frequencies, average salary by skill, and overall metrics."""
        if df.empty:
            return {"top_skills": {}, "metrics": {}}

        # Parse skills column or fallback to job_title
        if "skills" in df.columns:
            df["extracted_skills"] = df["skills"].apply(
                lambda x: self.extract_skills_from_text(x if isinstance(x, str) else " ".join(x) if isinstance(x, list) else "")
            )
        else:
            df["extracted_skills"] = df["job_title"].apply(self.extract_skills_from_text)

        all_skills = [skill for sublist in df["extracted_skills"] for skill in sublist]
        skill_counts = Counter(all_skills)

        # Basic summary metrics
        metrics = {
            "total_jobs": len(df),
            "remote_jobs_count": int(df["is_remote"].sum()) if "is_remote" in df.columns else len(df),
            "avg_market_salary": round(df["avg_salary"].dropna().mean(), 2) if "avg_salary" in df.columns and not df["avg_salary"].dropna().empty else None,
            "unique_skills_detected": len(skill_counts)
        }

        return {
            "skill_counts": dict(skill_counts.most_common(15)),
            "metrics": metrics,
            "processed_df": df
        }