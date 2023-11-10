import json
from datetime import datetime

# Constants
FILENAME = 'githubPR.json'
HTML_FILENAME = 'githubPR.html'

def generate_html_template(pull_requests):
    """Generates an HTML template for the pull requests."""
    html_content = """
<!DOCTYPE html>
<html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        th,
        td {
            text-align: center;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1 class="text-center mt-3 mb-4">Pull Request Dashboard</h1>
        <div class="table-responsive">
            <table class="table table-bordered table-striped">
                <thead class="thead-light">
                    <tr>
                        <th>PR Number</th>
                        <th>PR Title</th>
                        <th>PR Author</th>
                        <th>Created Date</th>
                        <th>Merged Date</th>
                    </tr>
                </thead>
                <tbody>
"""

    for pr in pull_requests:
        html_content += f"""
                    <tr>
                        <td>{pr['number']}</td>
                        <td>{pr['title']}</td>
                        <td>{pr['user']['login']}</td>
                        <td>{pr['created_at']}</td>
                        <td>{pr['merged_at'] if pr['merged_at'] else 'Not Merged'}</td>
                    </tr>
        """

    html_content += """
                </tbody>
            </table>
        </div>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>

</html>
"""

    with open(HTML_FILENAME, 'w') as file:
        file.write(html_content)

def main():
    """Main function of the script."""
    with open(FILENAME, 'r') as f:
        pull_requests = json.load(f)
    print("All PRs have been fetched.")

    # Generate HTML template
    generate_html_template(pull_requests)

# Runs the main function if the script is run directly
if __name__ == "__main__":
    main()