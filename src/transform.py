import os
import json
import pandas as pd
from glob import glob

RAW_FOLDER = "data/raw"
PROCESSED_FOLDER = "data/processed"

# Swiss cities (example)
CANTON_MAP = {
    "Zurich": "ZH",
    "Geneva": "GE",
    "Bern": "BE",
    "Basel": "BS",
    "Lausanne": "VD"
}

def clean_text(text: str) -> str:
    """Remove extra spaces and newlines"""
    if text:
        return " ".join(text.split())
    return ""

def extract_jobs_from_json(file_path: str) -> list:
    """Extract relevant job info from a raw JSON file"""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    jobs = []
    for item in data.get("results", []):
        job = {
            "job_id": item.get("id"),
            "title": clean_text(item.get("title")),
            "company": clean_text(item.get("company", {}).get("display_name")),
            "location": clean_text(item.get("location", {}).get("area")[-1] if item.get("location", {}).get("area") else None),
            "canton": CANTON_MAP.get(item.get("location", {}).get("area")[-1], None),
            "salary_min": item.get("salary_min"),
            "salary_max": item.get("salary_max"),
            "description": clean_text(item.get("description")),
            "date_posted": item.get("created")
        }
        jobs.append(job)
    return jobs

def main():
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)

    all_jobs = []
    for file in glob(os.path.join(RAW_FOLDER, "*.json")):
        all_jobs.extend(extract_jobs_from_json(file))

    df = pd.DataFrame(all_jobs)
    df.drop_duplicates(subset=["job_id"], inplace=True)
    
    output_file = os.path.join(PROCESSED_FOLDER, "swiss_jobs_clean.csv")
    df.to_csv(output_file, index=False)
    print(f"Clean data saved to {output_file}")

if __name__ == "__main__":
    main()
