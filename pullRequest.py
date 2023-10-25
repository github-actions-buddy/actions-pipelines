from github import Github
from datetime import datetime

# GitHub access token or username and password
ACCESS_TOKEN = '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'
REPO_NAME = 'Kiran-Waghamare/actions-pipelines'

g = Github(ACCESS_TOKEN)

repo = g.get_repo(REPO_NAME)

# Function to calculate days since created/opened
def days_since_created(created_at):
    created_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    today = datetime.now()
    return (today - created_date).days

# Function to filter and sort Pull Requests
def filter_and_sort_pull_requests(state, time_filter, sort_by):
    pull_requests = repo.get_pulls(state=state, sort='number', direction='asc')
    filtered_pull_requests = []
    for pr in pull_requests:
        created_date = pr.created_at.strftime("%Y-%m-%d")
        if time_filter == 'day':
            if created_date == datetime.now().strftime("%Y-%m-%d"):
                filtered_pull_requests.append(pr)
        elif time_filter == 'week':
            if (datetime.now() - pr.created_at).days <= 7:
                filtered_pull_requests.append(pr)
        elif time_filter == 'month':
            if (datetime.now() - pr.created_at).days <= 30:
                filtered_pull_requests.append(pr)
        elif time_filter == 'year':
            if (datetime.now() - pr.created_at).days <= 365:
                filtered_pull_requests.append(pr)

    if sort_by == 'number':
        filtered_pull_requests.sort(key=lambda x: x.number)
    elif sort_by == 'created':
        filtered_pull_requests.sort(key=lambda x: x.created_at)

    return filtered_pull_requests

# Generate HTML output
html_output = """
<!DOCTYPE html>
<html>
<head>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Pull Request Dashboard</h1>
    <table>
        <tr>
            <th>PR Number</th>
            <th>PR Title</th>
            <th>PR Author</th>
            <th>Created Date</th>
            <th>Merged Date</th>
            <th>Closed Date</th>
            <th>Days Since Created</th>
        </tr>
"""

# Example usage:
filtered_pull_requests = filter_and_sort_pull_requests('open', 'day', 'number')

for pr in filtered_pull_requests:
    html_output += f"""
        <tr>
            <td>{pr.number}</td>
            <td>{pr.title}</td>
            <td>{pr.user.login}</td>
            <td>{pr.created_at}</td>
            <td>{pr.merged_at if pr.merged_at else 'Not Merged'}</td>
            <td>{pr.closed_at if pr.closed_at else 'Not Closed'}</td>
            <td>{days_since_created(pr.created_at)}</td>
        </tr>
    """

html_output += """
    </table>
</body>
</html>
"""

with open('PullRequestDashboard.html', 'w') as file:
    file.write(html_output)
