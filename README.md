# Instagram Liking Bot

This bot automates logging into multiple Instagram accounts to like specific posts. It is built using Python and Selenium.

## Prerequisites

Before running the bot, ensure you have the following installed on your machine:
1.  **Python 3.7+**: Download and install from [python.org](https://www.python.org/downloads/).
2.  **Google Chrome**: The bot uses Chrome as its automated browser. Ensure Chrome is installed.

## Setup & Installation

1.  **Clone or Download the Repository**:
    Extract the files to a folder on your computer (e.g., `Desktop/instabot`).

2.  **Open a Terminal / Command Prompt**:
    Navigate to the folder where you extracted the files.
    ```bash
    cd path/to/instabot
    ```

3.  **Set up a Virtual Environment (Recommended but optional)**:
    It's best practice to use a virtual environment to avoid module conflicts.
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    ```

4.  **Install Python Dependencies**:
    Install the required libraries (`selenium`, `webdriver-manager`, `pandas`) by running:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Set up Credentials**:
    Open the `credentials.csv` file in a spreadsheet editor (like Excel or Google Sheets) or a text editor.
    Fill in your account details. The file MUST have the following headers on the first line exactly as shown:
    ```csv
    username,password,profile_url,post_url
    ```
    - `username`: Your Instagram username.
    - `password`: Your Instagram password.
    - `profile_url`: (Optional) The specific profile to visit before liking a post. Leave blank if not needed.
    - `post_url`: The direct link to the post you want to like (e.g., `https://www.instagram.com/p/B_.../`).

    *Example `credentials.csv`:*
    ```csv
    username,password,profile_url,post_url
    my_bot_account,SuperSecret123,https://www.instagram.com/target_profile/,https://www.instagram.com/p/ABCD123/
    ```

## Usage

Once everything is set up and your `credentials.csv` is populated, run the script:

```bash
python instabot.py
```

## Important Notes

- **Anti-Bot Measures**: Instagram is very strict against automation. This script uses a fresh incognito browser session for each login to minimize detection and adds random delays, but frequent logins/actions can still flag or ban your accounts. Use with caution.
- **Two-Factor Authentication (2FA)**: Two-Factor Authentication is currently **not supported**. Ensure 2FA is disabled for any accounts used by this bot.
- **Headless Mode**: The browser runs visibly by default so you can see what it is doing. To make it invisible, edit `instabot.py` and uncomment the line `# options.add_argument("--headless")` in the `setup_browser` function.
