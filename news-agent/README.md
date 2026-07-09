# Daily AI News Email Agent

A simple Python + LangGraph agent that fetches the latest news, summarizes it with OpenAI, builds a short email, and sends it through Gmail SMTP.

## Project Files

- `app.py` - runs the agent once and sends the email immediately
- `graph.py` - LangGraph workflow with fetch, summarize, create email, and send nodes
- `tools.py` - NewsAPI fetch logic and OpenAI summarization
- `email_sender.py` - Gmail SMTP email sender
- `scheduler.py` - daily scheduler that sends at a fixed time
- `requirements.txt` - Python dependencies
- `.env` - API keys and email settings

## Requirements

- Python 3.10 or newer
- NewsAPI key
- OpenAI API key
- Gmail account with 2-Step Verification enabled
- Gmail App Password

## Setup

1. Install dependencies:

```powershell
pip install -r requirements.txt
```

2. Fill in your `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-5
NEWSAPI_KEY=your_newsapi_key_here
GMAIL_USER=your_gmail_address@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password_here
TO_EMAIL=your_gmail_address@gmail.com
SEND_TIME=07:30
```

## How It Works

![Daily AI News workflow](assets/flowchart.svg)

## Run Once

Run the agent immediately and send one email:

```powershell
python app.py
```

## Run Daily Scheduler

Run the scheduler to send the email every day at the time in `SEND_TIME`:

```powershell
python scheduler.py
```

## GitHub Actions (Recommended)

Use GitHub Actions to run the agent daily without keeping a local machine running:

1. Push this repository to GitHub.
2. Go to your repository **Settings** → **Secrets and variables** → **Actions**.
3. Add the following repository secrets:
   - `OPENAI_API_KEY`
   - `OPENAI_MODEL` (e.g., `gpt-5`)
   - `NEWSAPI_KEY`
   - `GMAIL_USER`
   - `GMAIL_APP_PASSWORD`
   - `TO_EMAIL`
4. The workflow is configured to run daily at 07:30 UTC. You can also trigger it manually from the **Actions** tab.
5. To change the schedule time, edit `.github/workflows/daily-news.yml` and modify the cron expression.

## Notes

- `TO_EMAIL` is the address that receives the email.
- If you want to send to the same inbox as the Gmail login, set `TO_EMAIL` equal to `GMAIL_USER`.
- `SEND_TIME` uses 24-hour `HH:MM` format, for example `07:30`.
