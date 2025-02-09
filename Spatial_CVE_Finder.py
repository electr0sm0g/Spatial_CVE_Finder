import requests

print("")
print("################################################")
print("----------------Spatial_CVE_Finder--------------")
print("################################################")
print("----------------Bordel-Spatial-V1---------------")
print("################################################")
print("------------Test by: Etienne Lacoche------------")
print("---------Contact Twitter: @electr0sm0g----------")
print("################################################")
print("")

# Define GitHub API URL
GITHUB_API_URL = "https://api.github.com"

# Your GitHub personal access token
GITHUB_API_TOKEN = ''  # Replace with your actual token
headers = {
    'Authorization': f'token {GITHUB_API_TOKEN}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Function to search repositories with a query on GitHub
def search_repositories(query):
    repos = []
    url = f"{GITHUB_API_URL}/search/repositories?q={query}&type=repositories&per_page=100"
    
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            search_results = response.json()
            repos.extend(search_results['items'])  # Add the repositories from the current page
            if 'next' in response.links:
                url = response.links['next']['url']  # Get next page if available
            else:
                break
        else:
            print(f"Failed to fetch repositories: {response.status_code}")
            break
    
    return repos

# Function to get open issues with 'bug' or 'security' labels from a repository
def get_labeled_issues(repo_full_name, labels):
    issues = []
    url = f"{GITHUB_API_URL}/repos/{repo_full_name}/issues?state=open"  # Only fetch open issues
    
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            for issue in response.json():
                # Check if the issue has any of the specified labels
                issue_labels = [label['name'].lower() for label in issue.get('labels', [])]
                if any(label in issue_labels for label in labels):
                    issues.append(issue['html_url'])
            # Check for pagination to get all issues
            if 'next' in response.links:
                url = response.links['next']['url']
            else:
                break
        else:
            print(f"Failed to fetch issues for {repo_full_name}: {response.status_code}")
            break
    
    return issues

# Main function to get all labeled issues for all repositories from the search result
def get_all_labeled_issues(query, labels):
    all_labeled_issues = []
    
    # Step 1: Search repositories based on the query
    repos = search_repositories(query)
    
    # Step 2: Get all issues with the specified labels for each repository
    for repo in repos:
        repo_full_name = repo['full_name']  # e.g., 'owner/repo_name'
        print(f"Fetching open {', '.join(labels)} issues for repository: {repo_full_name}")
        labeled_issues = get_labeled_issues(repo_full_name, labels)
        all_labeled_issues.extend(labeled_issues)
    
    # Step 3: Write the URLs to a text file
    if all_labeled_issues:
        with open(f"{query}_open_issues.txt", "w") as file:
            for issue_url in all_labeled_issues:
                file.write(issue_url + "\n")
        print(f"\nAll labeled open issues URLs have been written to '{query}_open_issues.txt'.")
    else:
        print(f"No open labeled issues found for {', '.join(labels)}.")

# List of keywords related to satellites or software satellites
search_terms = [
    "cubesat", "nanosat", "nasa", 
    "software satellite", "software-defined satellite", 
    "software-defined radio", "software-controlled satellite", 
    "space software", "satellite software", 
    "satellite simulation", "satellite system design", 
    "spacecraft software", "mission control software",
    "embedded systems satellite", "embedded satellite software",
    "satellite firmware", "space software architecture", 
    "space robotics software", "communications satellite software",
    "navigation satellite software", "earth observation satellite software",
    "military satellite software", "navigation software satellite", 
    "AI satellite software", "autonomous satellite software", 
    "satellite machine learning", "satellite AI", "edge computing satellite"
]

# Expanded list of labels related to security or bugs
labels = [
    "bug", "security", "security vulnerability", "critical", "high priority", 
    "vulnerability", "security fix", "bug fix", "urgent", "fix", "patch"
]  # The labels to search for

# Query for each term and collect open issues
if __name__ == "__main__":
    for query in search_terms:
        print(f"\nSearching for open issues with {', '.join(labels)} labels in repositories for '{query}'...")
        get_all_labeled_issues(query, labels)

