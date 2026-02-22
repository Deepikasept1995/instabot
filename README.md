# Instagram Liking Bot

This bot automates logging into multiple Instagram accounts to like specific posts.

## Setup

1.  **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt (~/Desktop/instabot/.venv/bin/python)
    ```

2.  **Configure Credentials**:
    - Open `credentials.csv`.
    - Fill in your account details.
    - `username`: Your Instagram username.
    - `password`: Your Instagram password.
    - `profile_url`: (Optional) The profile to visit before liking.
    - `post_url`: The direct link to the post you want to like (e.g., `https://www.instagram.com/p/B_.../`).

## Usage

Run the script:
```bash
python instabot.py
```

## Important Notes

- **Anti-Bot Measures**: Instagram is very strict. This script uses a fresh browser session for each login to minimize detection, but frequent logins/actions can still flag your accounts. Use with caution.
- **2FA**: Two-Factor Authentication is not currently supported. Ensure it is disabled for these accounts or handle it manually during the script's `sleep` periods (though script is automated).
- **Headless Mode**: The browser runs visibly by default. To make it invisible, uncomment `options.add_argument("--headless")` in `instabot.py`.
