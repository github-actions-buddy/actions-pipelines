import json
import requests
from datetime import datetime


# Constants
URL_BASE = "https://api.github.com/repos/Kiran-Waghamare/actions-pipelines/pulls"
HEADERS = {'Authorization': 'Bearer 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'}
FILENAME = 'githubPR.json'

def fetch_pull_requests(page):
    """Fetches pull requests from the specified page."""
    params = {
        "state": "all",
        "sort": "created",
        "per_page": 100,
        "page": page
    }
    response = requests.get(URL_BASE, headers=HEADERS, params=params)
    response.raise_for_status()  # Raises an exception if the request fails
    return response.json()

def fetch_all_pull_requests():
    """Fetches all pull requests."""
    pull_requests = []
    for i in range(50):
        data = fetch_pull_requests(i)
        if data:
            print(f"Data found on page {i}; analyzing...")
            pull_requests.extend(data)
        else:
            break
    return pull_requests

def filter_pull_requests(pull_requests, start_date, end_date):
    """Filters pull requests that were merged between the start and end dates."""
    # Convert dates to datetime objects
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    filtered_pull_requests = []

    for pr in pull_requests:
        # Check if the pull request was merged
        if pr["merged_at"]:
            # Convert the merge date to a datetime object
            merge_date = datetime.strptime(pr["merged_at"], "%Y-%m-%dT%H:%M:%SZ")

            # Check if the merge date is within the specified range
            if start_date <= merge_date <= end_date:
                filtered_pull_requests.append(pr)

    return filtered_pull_requests

def write_to_file(data, filename):
    """Writes data to a file in JSON format."""
    with open(filename, 'w') as f:
        json.dump(data, f)

def main():
    """Main function of the script."""
    pull_requests = fetch_all_pull_requests()
    write_to_file(pull_requests, FILENAME)
    print("All PRs have been fetched.")
    
    # ------------ Uncomment to filter by date ------------
    # start_date = "2023-01-01"
    # end_date = "2023-12-31"
    # filtered_pull_requests = filter_pull_requests(pull_requests, start_date, end_date)
    # print(filtered_pull_requests)

# Runs the main function if the script is run directly
if __name__ == "__main__":
    main()