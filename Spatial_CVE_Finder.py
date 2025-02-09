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
print("----------------Bordel-Spatial-V1---------------")
print("################################################")
print("------------Test by: Etienne Lacoche------------")
print("---------Contact Twitter: @electr0sm0g----------")
print("################################################")
print("")


# Définir les URL de l'API GitHub et la clé d'authentification
GITHUB_API_URL = "https://api.github.com"
GITHUB_API_TOKEN = ''  # Remplacez par votre token
headers = {
    'Authorization': f'token {GITHUB_API_TOKEN}',
    'User-Agent': 'Mozilla/5.0'
}

# Connexion à la base de données SQLite
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

# Fonction pour insérer un problème dans la base de données
def insert_issue(conn, repo_name, issue_url, label, status):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO issues (repo_name, issue_url, label, status)
    VALUES (?, ?, ?, ?)
    ''', (repo_name, issue_url, label, status))
    conn.commit()

# Fonction pour vérifier si le problème existe déjà dans la base de données
def issue_exists(conn, issue_url):
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM issues WHERE issue_url = ?
    ''', (issue_url,))
    return cursor.fetchone() is not None

# Fonction pour envoyer une notification par e-mail (groupé)
def send_email(subject, body, to_email):
    from_email = "your_email@example.com"
    password = "your_email_password"  # Remplacez par votre mot de passe ou utilisez un mot de passe spécifique à l'application
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
    
    print("E-mail envoyé à", to_email)

# Fonction pour vérifier et gérer le quota de l'API GitHub
def check_rate_limit():
    url = "https://api.github.com/rate_limit"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        remaining = data['resources']['core']['remaining']
        reset_time = data['resources']['core']['reset']
        if remaining == 0:
            # Si les requêtes restantes sont 0, on attend jusqu'à ce que la limite se réinitialise
            reset_time = reset_time - time.time()  # Calcul du temps restant jusqu'à la réinitialisation
            print(f"Taux de requêtes épuisé. Attente de {int(reset_time)} secondes...")
            time.sleep(reset_time + 10)  # Attendre un peu plus longtemps pour s'assurer de la réinitialisation
        else:
            print(f"Il vous reste {remaining} requêtes avant la limite.")
    else:
        print(f"Erreur de récupération du quota de requêtes: {response.status_code}")
        time.sleep(60)  # Attente en cas d'erreur de récupération du quota

# Fonction pour rechercher des dépôts sur GitHub
def search_repositories(query):
    repos = []
    url = f"{GITHUB_API_URL}/search/repositories?q={query}&type=repositories&per_page=100"
    
    while url:
        check_rate_limit()  # Vérifier et gérer le taux de requêtes
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            search_results = response.json()
            repos.extend(search_results['items'])
            if 'next' in response.links:
                url = response.links['next']['url']
            else:
                break
        else:
            print(f"Erreur lors de la récupération des dépôts : {response.status_code}")
            break
    return repos

# Fonction pour récupérer les problèmes avec les étiquettes spécifiées
def get_labeled_issues(repo_full_name, labels, conn):
    issues = []
    url = f"{GITHUB_API_URL}/repos/{repo_full_name}/issues?state=open"
    
    while url:
        check_rate_limit()  # Vérifier et gérer le taux de requêtes
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            for issue in response.json():
                issue_labels = [label['name'].lower() for label in issue.get('labels', [])]
                if any(label in issue_labels for label in labels):
                    if not issue_exists(conn, issue['html_url']):
                        insert_issue(conn, repo_full_name, issue['html_url'], ', '.join(issue_labels), issue['state'])
                        issues.append(issue['html_url'])
            if 'next' in response.links:
                url = response.links['next']['url']
            else:
                break
        else:
            print(f"Erreur lors de la récupération des problèmes pour {repo_full_name}: {response.status_code}")
            break
    return issues

# Fonction principale pour récupérer toutes les issues labellisées et mettre à jour la base de données
def get_all_labeled_issues(query, labels):
    conn = init_db()
    repos = search_repositories(query)
    
    all_labeled_issues = []
    for repo in repos:
        repo_full_name = repo['full_name']
        print(f"Recherche des problèmes ouverts dans {repo_full_name}...")
        labeled_issues = get_labeled_issues(repo_full_name, labels, conn)
        all_labeled_issues.extend(labeled_issues)
    
    # Envoyer un e-mail groupé avec tous les problèmes trouvés
    if all_labeled_issues:
        email_body = "\n".join(all_labeled_issues)
        send_email(
            "Résumé des problèmes GitHub trouvés", 
            f"Voici tous les problèmes labellisés trouvés :\n\n{email_body}", 
            "votre_email@example.com"
        )
        print(f"\nTotal des problèmes trouvés : {len(all_labeled_issues)}")
    else:
        print("Aucun problème labellisé trouvé.")

if __name__ == "__main__":
    search_terms = [
        "cubesat", "nanosat", "satellite software", "space software", "software-defined satellite",
        "nanosatellites", "cubesat", "space mission", "satellite communications",
        "ground station", "space telemetry", "orbital simulation",
        "satellite security", "satellite software vulnerabilities", "GNSS"
    ]
    
    labels = [
        "bug", "critical bug", "security", "high priority", "security fix", 
        "bugfix", "regression", "vulnerability", "security vulnerability", 
        "high security risk", "needs fix", "exploit", "error", "defect", 
        "privacy", "data breach"
    ]
    
    for term in search_terms:
        get_all_labeled_issues(term, labels)
