import re
import pandas as pd
from typing import Optional, Tuple

class DataCleaner:
    @staticmethod
    def parse_salary(salary_raw: Optional[str]) -> Tuple[Optional[float], Optional[float]]:
        """Parses raw salary strings like '$80k - $120k' or '$90,000/yr' into (min, max) floats."""
        if not salary_raw or pd.isna(salary_raw):
            return None, None
        
        text = str(salary_raw).replace(",", "").lower()
        numbers = re.findall(r"(\d+(?:\.\d+)?)(\s*k)?", text)
        
        extracted = []
        for val, is_k in numbers:
            try:
                num = float(val)
                if is_k or num < 1000:
                    num *= 1000
                extracted.append(num)
            except ValueError:
                continue
                
        if len(extracted) >= 2:
            return min(extracted[:2]), max(extracted[:2])
        elif len(extracted) == 1:
            return extracted[0], extracted[0]
        return None, None

    def clean_jobs_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans and standardizes raw job listings DataFrame."""
        if df.empty:
            return pd.DataFrame()

        clean_df = df.copy()

        # 1. Deduplicate by job title and company
        clean_df = clean_df.drop_duplicates(subset=["job_title", "company"], keep="first")

        # 2. Clean whitespace and fill missing strings
        string_cols = ["job_title", "company", "location", "job_url"]
        for col in string_cols:
            if col in clean_df.columns:
                clean_df[col] = clean_df[col].astype(str).str.strip()
                clean_df[col] = clean_df[col].replace({"nan": "Not Specified", "None": "Not Specified", "": "Not Specified"})
            else:
                clean_df[col] = "Not Specified"

        # 3. Standardize salaries
        if "salary" in clean_df.columns:
            salary_parsed = clean_df["salary"].apply(self.parse_salary)
            clean_df["min_salary"] = [s[0] for s in salary_parsed]
            clean_df["max_salary"] = [s[1] for s in salary_parsed]
            clean_df["avg_salary"] = clean_df[["min_salary", "max_salary"]].mean(axis=1)
        else:
            clean_df["min_salary"] = None
            clean_df["max_salary"] = None
            clean_df["avg_salary"] = None

        # 4. Standardize remote location flag
        if "location" in clean_df.columns:
            clean_df["is_remote"] = clean_df["location"].str.lower().str.contains("remote|anywhere|worldwide", na=False)
        else:
            clean_df["is_remote"] = True

        return clean_df