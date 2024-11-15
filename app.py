# app.py
from flask import Flask, request, jsonify
import requests
from datetime import datetime
from config import GITHUB_TOKEN  

app = Flask(__name__)

def suggest_profile_improvements(username):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'https://api.github.com/users/{username}'
    response = requests.get(url, headers=headers)
    profile_data = response.json()

    tips = []

    # Check for profile picture
    if not profile_data.get('avatar_url'):
        tips.append('Add a professional profile picture.')

    # Check for bio
    if not profile_data.get('bio'):
        tips.append('Add a professional bio in the overview section.')

    # Check for blog or portfolio link
    if not profile_data.get('blog'):
        tips.append('Include links to personal projects and portfolio in your profile.')

    # Fetch repositories
    repos_url = f'https://api.github.com/users/{username}/repos'
    repos_response = requests.get(repos_url, headers=headers)
    repos_data = repos_response.json()

    # Check for repository updates
    recent_update = False
    now = datetime.now()
    for repo in repos_data:
        last_updated = datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        if (now - last_updated).days < 30:
            recent_update = True
            break
    if not recent_update:
        tips.append('Regularly update repositories with recent work.')

    # Check for descriptive commit messages
    commit_messages_descriptive = True
    for repo in repos_data:
        commits_url = f'https://api.github.com/repos/{username}/{repo["name"]}/commits'
        commits_response = requests.get(commits_url, headers=headers)
        commits_data = commits_response.json()
        for commit in commits_data:
            message = commit['commit']['message']
            if len(message.split()) < 3:
                commit_messages_descriptive = False
                break
        if not commit_messages_descriptive:
            break
    if not commit_messages_descriptive:
        tips.append('Use descriptive commit messages and maintain a consistent commit history.')

    # Check for open-source contributions
    events_url = f'https://api.github.com/users/{username}/events'
    events_response = requests.get(events_url, headers=headers)
    events_data = events_response.json()
    contributed_to_open_source = any(event['type'] == 'PullRequestEvent' for event in events_data)
    if not contributed_to_open_source:
        tips.append('Participate in open-source projects and contribute to community discussions.')

    return tips

def get_repositories_info(username):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url, headers=headers)
    repos_data = response.json()
    repos_info = []
    for repo in repos_data:
        repos_info.append({
            'repo_name': repo['name'],
            'language': repo['language'],
            'description': repo.get('description', 'No description available'),
            'stargazers_count': repo['stargazers_count'],
            'forks_count': repo['forks_count']
        })
    return repos_info

def rate_github_profile(username):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'https://api.github.com/users/{username}'
    response = requests.get(url, headers=headers)
    profile_data = response.json()

    followers = profile_data.get('followers', 0)
    public_repos = profile_data.get('public_repos', 0)
    bio = profile_data.get('bio', '') or ''

    repos_info = get_repositories_info(username)
    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_info)
    total_forks = sum(repo.get('forks_count', 0) for repo in repos_info)

    followers_score = min(followers / 5000, 1.0) * 4
    public_repos_score = min(public_repos / 200, 1.0) * 3
    stars_score = min(total_stars / 1000, 1.0) * 2
    forks_score = min(total_forks / 500, 1.0) * 1

    bio_rating = min(len(bio.split()) * 10, 100) / 100
    repo_description_rating = len([repo for repo in repos_info if repo.get('description') and len(repo['description'].split()) > 4]) / len(repos_info) if repos_info else 0
    backlink_rating = (bool(bio) + bool(profile_data.get('location')) + bool(profile_data.get('blog')) + bool(profile_data.get('company'))) / 4

    rating = (followers_score + public_repos_score + stars_score + forks_score +
              bio_rating + repo_description_rating + backlink_rating)

    return round(min(rating, 10), 2)

@app.route('/analyze_profile', methods=['POST'])
def analyze_profile():
    data = request.json
    username = data.get('username')

    # Rate the profile
    rating = rate_github_profile(username)

    # Get improvement suggestions
    improvements = suggest_profile_improvements(username)

    # Fetch additional profile information
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'https://api.github.com/users/{username}'
    response = requests.get(url, headers=headers)
    profile_data = response.json()

    profile_name = profile_data.get('login', 'N/A')
    followers = profile_data.get('followers', 0)

    # Determine predominant tech stack
    repos_info = get_repositories_info(username)
    languages = [repo['language'] for repo in repos_info if repo['language']]
    predominant_tech_stack = ', '.join(set(languages))

    result = {
        "Profile Name": profile_name,
        "Followers": followers,
        "Predominant Tech Stack": predominant_tech_stack,
        "Rating": rating,
        "Profile Improvement Tips": improvements
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
