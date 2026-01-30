import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Adzuna API credentials from environment variables
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

# Base URL for Adzuna API
BASE_URL = "https://api.adzuna.com/v1/api/jobs"
COUNTRY = "ch"  # Switzerland


def fetch_jobs(page: int = 1, results_per_page: int = 50):
    """
    Fetch job listings from Adzuna API.
    """
    # Construct the API endpoint URL for the given page
    url = f"{BASE_URL}/{COUNTRY}/search/{page}"

    # Parameters for the API request
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": results_per_page,
        "content-type": "application/json",
    }

    # Make GET request to Adzuna API
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise error if request fails

    # Return JSON response as Python dictionary
    return response.json()


def save_raw_data(data: dict):
    """
    Save raw JSON response to data/raw folder with timestamp.
    """
    # Create a timestamp string for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/raw/jobs_raw_{timestamp}.json"

    # Ensure the directory exists
    os.makedirs("data/raw", exist_ok=True)

    # Write JSON data to file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Raw data saved to {filename}")


def main():
    # Check if API credentials are set
    if not APP_ID or not APP_KEY:
        raise ValueError("Missing Adzuna API credentials")

    # Fetch job listings
    print("Fetching job listings from Adzuna API...")
    data = fetch_jobs(page=1)

    # Save the raw data to file
    save_raw_data(data)


# Run the script when executed directly
if __name__ == "__main__":
    main()
