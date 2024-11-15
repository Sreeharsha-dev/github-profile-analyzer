# GitHub Profile Analyzer

The GitHub Profile Analyzer is a Flask-based application that helps analyze GitHub user profiles, provides improvement suggestions, and rates profiles based on various factors. It leverages the GitHub API to gather profile and repository information, then uses custom logic to suggest enhancements for creating a stronger GitHub profile.

## Features

- **Profile Analysis**: Evaluates various aspects of a GitHub profile, including followers, bio, profile picture, and repository activity.
- **Improvement Suggestions**: Recommends improvements such as adding a profile picture, bio, or updating repositories with recent work.
- **Profile Rating**: Scores profiles on a scale of 1-10 based on follower count, repository activity, star count, and other parameters.
- **Predominant Tech Stack**: Identifies the most used languages in the user's repositories.

## Prerequisites

- Python 3.7+
- GitHub personal access token with permissions for public data (if accessing private data, adjust token permissions).

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/github-profile-analyzer.git
   cd github-profile-analyzer
   ```

2. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up GitHub token**:
   - Create a `.env` file in the project directory:
   
     ```bash
     touch .env
     ```

   - Open `.env` and add your GitHub token:

     ```plaintext
     GITHUB_TOKEN=your_github_token_here
     ```

## Project Structure

```
github-profile-analyzer/
├── app.py                    # Main Flask application code
├── config.py                 # Configuration file for GitHub token
├── requirements.txt          # Dependencies
├── README.md                 # Documentation
└── .env                      # Environment file for sensitive information (like GitHub token)
```

### Explanation of Files

- **app.py**: Contains the main application logic for analyzing profiles.
- **config.py**: Loads environment variables, including the GitHub token.
- **.env**: Stores sensitive information like the GitHub token (excluded from version control).
- **requirements.txt**: Lists project dependencies.

## Usage

1. **Start the Flask server**:

   ```bash
   python app.py
   ```

2. **Analyze a GitHub Profile**:

   Send a `POST` request to `http://127.0.0.1:5000/analyze_profile` with JSON data containing the GitHub username.

   Example:

   ```json
   POST http://127.0.0.1:5000/analyze_profile
   Content-Type: application/json

   {
     "username": "octocat"
   }
   ```

3. **Response**:

   The API will return a JSON response with profile details, rating, predominant tech stack, and improvement tips.

   ```json
   {
     "Profile Name": "octocat",
     "Followers": 500,
     "Predominant Tech Stack": "Python, JavaScript",
     "Rating": 8.2,
     "Profile Improvement Tips": [
       "Add a professional profile picture.",
       "Include links to personal projects and portfolio in your profile."
     ]
   }
   ```

## Example Output

| Field                  | Description                                                   |
|------------------------|---------------------------------------------------------------|
| **Profile Name**       | GitHub username                                              |
| **Followers**          | Number of followers                                          |
| **Predominant Tech Stack** | Primary languages used in repositories                      |
| **Rating**             | Profile score (out of 10)                                    |
| **Profile Improvement Tips** | Suggestions to improve the profile                        |

## Notes

- The rating and suggestions are based on profile activity, description quality, and consistency in the repository. The scoring criteria prioritize a well-maintained profile.
- To avoid API rate limits, ensure your GitHub token has the necessary permissions for accessing user and repository data.

## Contributing

If you’d like to contribute, please fork the repository and create a pull request with your changes. Ensure all code changes are properly documented and tested.

## License

This project is open-source and available under the MIT License.
