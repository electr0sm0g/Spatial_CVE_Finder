# Spatial_CVE_Finder

Little GitHub Scraper Tool for Finding CVEs in Aerospace More Easily

![](https://github.com/electr0sm0g/Spatial_CVE_Finder/blob/main/Screenshot%202025-02-09%20at%2018.15.20.png)

Contact Twitter: @electr0sm0g

GitHub Issue Tracker & Notification System

This Python-based project allows you to track issues labeled with "bug" or "security" across multiple GitHub repositories based on a search query. It handles rate limiting, checks if an issue already exists in the database, and sends email notifications when new issues are found.

Features:

Search GitHub repositories using keywords (e.g., cubesat, nanosat, nasa, satellite software).
Filter issues with specific labels like "bug" or "security".
Store issue details in a local SQLite database to avoid duplicates.
Send email notifications whenever a new "bug" or "security" issue is found.

Handle GitHub API rate limits: 

The script automatically checks and waits for the rate limit to reset if exceeded.

Requirements

Python 3.x
requests library (for interacting with GitHub API)
sqlite3 library (for database management)
smtplib (for email notifications)

To install the necessary dependencies, run:

pip install requests

Setup

GitHub Personal Access Token:

You need a GitHub personal access token for authentication. Generate it from your GitHub account settings.
Replace GITHUB_API_TOKEN in the script with your generated token.

Email Setup:

Update the send_email function with your email credentials (from_email, password) to send notifications.
You can use an app-specific password for Gmail or other providers if necessary.

SQLite Database:

The system uses a local SQLite database (github_issues.db) to store issue data and avoid processing duplicate issues.

How It Works

Search Repositories:

The script searches repositories on GitHub based on specific keywords like cubesat, nanosat, nasa, etc.
It supports multiple search queries and can handle a list of terms.

Get Issues:

For each repository found, the script fetches all open issues that have labels such as "bug" or "security".
The script ensures that issues are not processed again by checking if they already exist in the database.

Rate Limiting:

The script automatically checks the current rate limit status of the GitHub API.
If the rate limit is reached, the script will wait for the reset time before proceeding with further requests.

Email Notifications:

Whenever a new issue with the required label is found, the script sends an email notification to the specified email address.
Database Structure

The SQLite database (github_issues.db) contains a table named issues with the following columns:

id: A unique identifier for each issue (primary key).
repo_name: The name of the repository where the issue was found.
issue_url: The URL of the issue.
label: The labels associated with the issue (e.g., "bug", "security").
status: The status of the issue (open or closed).

Code Walkthrough

check_rate_limit()
This function checks the current rate limit from GitHub's API and waits if the limit is reached.`

search_repositories(query)
This function performs a search query on GitHub for repositories based on the search terms (like cubesat, nanosat).
It handles pagination to retrieve all repositories if there are more than 100 results.

get_labeled_issues(repo_full_name, labels, conn)
For each repository, this function retrieves all open issues with specified labels (bug, security) from the repository.
It also checks if the issue is already stored in the database to avoid processing duplicates.
If a new issue is found, it sends an email notification.

insert_issue(conn, repo_name, issue_url, label, status)
Inserts the new issue information into the database.

issue_exists(conn, issue_url)
Checks if an issue is already stored in the database by comparing the issue URL.

send_email(subject, body, to_email)
Sends an email notification when a new issue is found.

init_db()
Initializes the SQLite database with the necessary table (issues) if it doesn’t already exist.

get_all_labeled_issues(query, labels)
The main function that orchestrates the entire process: searches repositories, retrieves issues, and sends email notifications.

How to Run
To run the script, simply execute it from the command line:

python github_issue_tracker.py

This will initiate the search for repositories and issues based on predefined keywords and labels.

Example Usage:

Edit
search_terms = ["cubesat", "nanosat", "nasa", "satellite software", "software-defined satellite"]
labels = ["bug", "security"]

for term in search_terms:
    get_all_labeled_issues(term, labels)
    
Handling Errors

Rate Limiting: If the rate limit is reached, the script waits until the limit is reset.

Database: If an issue already exists in the database, it will not be processed again.

Email: If the email cannot be sent, an error message will be displayed.

Future Improvements

Multi-threading: To speed up the processing of repositories and issues, you could add multi-threading or multiprocessing.

Enhanced Notifications: You could add support for multiple notification types (e.g., Slack, SMS) or configure different email templates for different types of issues.

Error Logging: Implement a logging system to track errors and retries.

Command-Line Interface (CLI): A more advanced user interface that allows for better customization of search queries, labels, and email settings.

License

This project is licensed under the MIT License - see the LICENSE file for details.
