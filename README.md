# Spatial_CVE_Finder

## Little GitHub Scraper Tool for Finding Vulnerabilities in Aerospace More Easily

![](https://github.com/electr0sm0g/Spatial_CVE_Finder/blob/main/Screenshot%202025-02-09%20at%2018.15.20.png)

## Contact Twitter: @electr0sm0g

# Spatial_CVE_Finder

### Description

**Spatial_CVE_Finder** is a tool designed to scrape GitHub repositories for issues related to vulnerabilities in aerospace-related projects. The tool looks for GitHub issues labeled with specific security-related terms (e.g., "critical bug," "vulnerability," "security risk") and sends an email notification if any relevant issues are found.

This project is useful for cybersecurity researchers, aerospace engineers, and developers who need to stay informed about vulnerabilities in the aerospace-related sector. The tool automates the process of searching for vulnerabilities, saving time and effort in manually monitoring relevant repositories.

### Features

- Searches for aerospace-related GitHub repositories based on keywords.
- Filters GitHub issues based on specific labels related to security vulnerabilities (e.g., "security vulnerability", "high priority").
- Automatically sends email notifications with details of any identified issues.
- Stores found issues in a SQLite database to prevent duplicate processing.
- Handles GitHub API rate limits and retries automatically.

---

### Prerequisites

- **Python 3.x** or higher
- Required Python packages: `requests`, `sqlite3`, `smtplib`

You can install the required packages using pip:

pip install requests sqlite3 smtplib


### Setup

1. **Clone the repository**:
   
   Clone the repository to your local machine:
   
git clone https://github.com/your-username/Spatial_CVE_Finder.git cd Spatial_CVE_Finder


2. **GitHub API Token**:

- You will need to create a GitHub API token for authentication.
- Visit [GitHub Tokens](https://github.com/settings/tokens) and create a new personal access token with the `repo` and `read:org` scopes.

Replace `your_github_token` in the code with your generated API token.

3. **Email Setup**:

The script sends email notifications using SMTP. For Gmail:
- Enable **"Less Secure Apps"** or use an **App-Specific Password**.
- Replace `your_email@example.com` and `your_app_specific_password` in the script with your email and app-specific password.

4. **Running the Script**:

To run the tool, simply execute the script:

python spatial_cve_finder.py


The tool will start searching for relevant GitHub issues based on the specified terms and labels, and it will send email notifications if any matching issues are found.

---

### How It Works

1. **Searching Repositories**:
The tool searches GitHub for repositories related to aerospace and satellite software by using keywords such as "cubesat", "satellite security", and "space telemetry".

2. **Checking for Labeled Issues**:
It looks for issues with security-related labels like "critical bug", "security", and "high priority". If an issue with one of these labels is found, it is logged and saved in an SQLite database.

3. **Email Notification**:
Once relevant issues are identified, an email containing the details of these issues is sent to the user’s email address.

4. **Database Management**:
All identified issues are stored in a local SQLite database to avoid duplicate entries.

---

### Configuration

- **Search Terms**: Modify the `search_terms` list to include any additional keywords related to aerospace projects you want to track.
- **Labels**: Customize the `labels` list to include any other issue labels you want to filter on.
- **Email**: Ensure you update the `mail` and `password` variables with your email and app-specific password for sending notifications.

---

### Contributing

Contributions are welcome! Feel free to fork the repository, open issues, and submit pull requests.

---

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Author

- **Etienne Lacoche**
  - [LinkedIn](https://fr.linkedin.com/in/etiennelacoche)
  - Twitter: [@electr0sm0g](https://twitter.com/electr0sm0g)



