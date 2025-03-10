import requests
import time
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("")
print("################################################")
print("----------------Spatial_CVE_Finder--------------")
print("################################################")
print("----------------Etienne Lacoche-----------------")
print("---https://fr.linkedin.com/in/etiennelacoche----")
print("---------Contact Twitter: @electr0sm0g----------")
print("################################################")
print("")

# Define GitHub API URLs and authentication token
GITHUB_API_URL = "https://api.github.com"
GITHUB_API_TOKEN = 'your_github_token'  # Replace with your GitHub API key

mail = "your_email@example.com"  # Use your email address
password = "your_app_specific_password"  # Use the app-specific password here

headers = {
    'Authorization': f'token {GITHUB_API_TOKEN}',
    'User-Agent': 'Mozilla/5.0'
}

# SQLite database connection
def init_db():
    conn = sqlite3.connect('github_issues.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS issues (
        id INTEGER PRIMARY KEY,
        repo_name TEXT,
        issue_url TEXT,
        label TEXT,
        status TEXT
    )
    ''')
    conn.commit()
    return conn

# Function to insert an issue into the database
def insert_issue(conn, repo_name, issue_url, label, status):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO issues (repo_name, issue_url, label, status)
    VALUES (?, ?, ?, ?)
    ''', (repo_name, issue_url, label, status))
    conn.commit()

# Function to check if the issue already exists in the database
def issue_exists(conn, issue_url):
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM issues WHERE issue_url = ?
    ''', (issue_url,))
    return cursor.fetchone() is not None

def send_email(subject, body, to_email):   
    msg = MIMEMultipart()
    msg['From'] = mail
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(mail, password)  # Use app password here
        server.sendmail(mail, to_email, msg.as_string())
    
    print("E-mail sent to", to_email)

# Function to check and manage GitHub API rate limit
def check_rate_limit():
    url = "https://api.github.com/rate_limit"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        remaining = data['resources']['core']['remaining']
        reset_time = data['resources']['core']['reset']
        if remaining == 0:
            # If no requests are left, wait until the limit resets
            reset_time = reset_time - time.time()  # Calculate time until reset
            print(f"Rate limit exhausted. Waiting for {int(reset_time)} seconds...")
            time.sleep(reset_time + 10)  # Wait a little longer to ensure reset
        else:
            print(f"{remaining} requests remaining before rate limit.")
    else:
        print(f"Error fetching rate limit: {response.status_code}")
        time.sleep(60)  # Wait if there's an error fetching the rate limit

# Function to search repositories on GitHub
def search_repositories(query):
    repos = []
    url = f"{GITHUB_API_URL}/search/repositories?q={query}&type=repositories&per_page=100"
    
    while url:
        check_rate_limit()  # Check and manage rate limit
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            search_results = response.json()
            repos.extend(search_results['items'])
            if 'next' in response.links:
                url = response.links['next']['url']
            else:
                break
        else:
            print(f"Error retrieving repositories: {response.status_code}")
            break
    return repos
# Function to retrieve issues with specified labels
def get_labeled_issues(repo_full_name, labels, conn):
    issues = []
    url = f"{GITHUB_API_URL}/repos/{repo_full_name}/issues?state=open"
    
    while url:
        check_rate_limit()  # Check and manage rate limit
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            for issue in response.json():
                # Debugging: Print the issue structure to understand its content
                print("DEBUGGING: Issue structure: ", issue)  
                
                # Extract labels from the issue correctly
                issue_labels = [label['name'].lower() for label in issue.get('labels', [])]
                
                if any(label in issue_labels for label in labels):
                    if not issue_exists(conn, issue['html_url']):
                        insert_issue(conn, repo_full_name, issue['html_url'], ', '.join(issue_labels), issue['state'])
                        issues.append(issue)
            if 'next' in response.links:
                url = response.links['next']['url']
            else:
                break
        else:
            print(f"Error retrieving issues for {repo_full_name}: {response.status_code}")
            break
    return issues

# Main function to retrieve all labeled issues and update the database
def get_all_labeled_issues(query, labels):
    conn = init_db()
    repos = search_repositories(query)
    
    all_labeled_issues = []
    for repo in repos:
        repo_full_name = repo['full_name']
        print(f"Searching for open issues in {repo_full_name}...")
        labeled_issues = get_labeled_issues(repo_full_name, labels, conn)
        all_labeled_issues.extend(labeled_issues)
    
    if all_labeled_issues:
        print(f"\nTotal issues found: {len(all_labeled_issues)}")
        
        # Generate the email body with all the issues found
        email_body = "\n\n".join([
            f"Repository: {issue['html_url']}\n"  # Use issue URL for repo info (or adjust as needed)
            f"Issue: {issue['html_url']}\n"
            f"Labels: {', '.join([label['name'] for label in issue.get('labels', [])])}\n\n"
            for issue in all_labeled_issues
        ])
        
        send_email("New Issues Found", email_body, mail)  # Send email with the issue details
    else:
        print("No labeled issues found.")

if __name__ == "__main__":
    search_terms = [
        "cubesat", "nanosat", "satellite software", "space software", "software-defined satellite",
        "nanosatellites", "space mission", "satellite communications",
        "ground station", "space telemetry", "orbital simulation",
        "satellite security", "satellite software vulnerabilities", "GNSS"
    ]
    
    labels = [
        "bug", "security", "high priority", "security fix", 
        "bugfix", "regression", "vulnerability", "security vulnerability", 
        "high security risk", "needs fix", "exploit", "error", "defect", 
        "privacy", "data breach"
    ]
    
    for term in search_terms:
        get_all_labeled_issues(term, labels)
