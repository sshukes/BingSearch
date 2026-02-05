# Bing Search Bot

This project runs a list of Bing searches using a **persistent browser profile** so your signed-in Bing account is reused between sessions. That ensures searches are associated with your account for credit.

> **Important:** You must sign in manually on the first run. The script reuses the same profile directory on subsequent runs.

## Setup

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

2. Add your queries to `queries.txt` (one per line).

## Usage

```bash
python bing_search_bot.py --queries queries.txt --profile-dir .bing-profile --delay 3
```

### First run login

- The browser opens with a fresh profile.
- Sign in to Bing/Microsoft in that window.
- Close the browser window to end the session.
- The profile is saved in `.bing-profile` and reused next time.

## Notes

- Keep the `.bing-profile` directory safe; it contains cookies/session data.
- Be mindful of Bing/Microsoft terms of service and your account policies.
