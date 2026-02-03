import os
import pandas as pd

PROCESSED_FOLDER = "data/processed"
INPUT_FILE = os.path.join(PROCESSED_FOLDER, "swiss_jobs_clean.csv")
OUTPUT_FILE = os.path.join(PROCESSED_FOLDER, "swiss_jobs_final.csv")

# Define the skills to extract
SKILLS = [
    "python", "sql", "excel", "power bi", "tableau",
    "machine learning", "aws", "docker", "java", "r", "spark", "git"
]

def extract_skills(description: str) -> str:
    """Return comma-separated skills found in description"""
    if not description:
        return ""
    description_lower = description.lower()
    found_skills = [skill for skill in SKILLS if skill in description_lower]
    return ", ".join(found_skills)

def main():
    # Read cleaned CSV
    df = pd.read_csv(INPUT_FILE)

    # Extract skills
    df["skills_extracted"] = df["description"].apply(extract_skills)

    # Save final CSV
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Final dataset saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
