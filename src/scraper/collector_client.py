import os
import time
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# Explicitly load .env from the project root directory
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class SkillRadarCollector:
    def __init__(self):
        self.api_token = os.getenv("BRIGHT_DATA_API_TOKEN")
        self.collector_id = os.getenv("COLLECTOR_ID")
        
        # Diagnostic check to ensure variables are loaded
        if not self.api_token:
            raise ValueError(f"❌ Missing BRIGHT_DATA_API_TOKEN. Checked path: {env_path}")
        if not self.collector_id:
            raise ValueError(f"❌ Missing COLLECTOR_ID. Checked path: {env_path}")
            
        print(f"✓ Authenticating with Collector ID: {self.collector_id}")
        self.base_url = "https://api.brightdata.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def fetch_jobs(self, target_url: str = "https://weworkremotely.com/categories/remote-programming-jobs") -> pd.DataFrame:
        """Triggers the Scraper Studio collector and polls for structured output."""
        trigger_endpoint = f"{self.base_url}/dca/trigger?collector={self.collector_id}&queue_next=1"
        payload = [{"url": target_url}]
        
        print("⚡ Triggering Scraper Studio collector...")
        res = requests.post(trigger_endpoint, headers=self.headers, json=payload)
        
        if res.status_code != 200:
            print(f"API Error Response: {res.text}")
        res.raise_for_status()
        
        collection_id = res.json().get("collection_id")
        print(f"✓ Collection job queued: {collection_id}")

        dataset_endpoint = f"{self.base_url}/dca/dataset?id={collection_id}"
        print("⏳ Polling for structured data...")
        
        for attempt in range(25):
            time.sleep(5)
            data_res = requests.get(dataset_endpoint, headers=self.headers)
            if data_res.status_code == 200:
                data = data_res.json()
                if data:
                    print(f"✓ Success: Retrieved {len(data)} records!")
                    return pd.DataFrame(data)
            print(f"  Extraction in progress... (attempt {attempt + 1}/25)")
            
        raise TimeoutError("Data collection timed out.")

if __name__ == "__main__":
    collector = SkillRadarCollector()
    df = collector.fetch_jobs()
    print("\n--- Extracted Sample ---")
    print(df.head())