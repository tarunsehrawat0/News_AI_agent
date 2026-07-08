import os
import time

import schedule
from dotenv import load_dotenv

from app import run_news_agent

load_dotenv()


def send_daily_news() -> None:
    """Run the news agent once and print a short status line."""
    email_text = run_news_agent()
    print("Daily email sent successfully.")
    print(email_text)


def main() -> None:
    """Schedule the daily email at the time stored in SEND_TIME."""
    send_time = os.getenv("SEND_TIME", "09:00")
    schedule.every().day.at(send_time).do(send_daily_news)

    print(f"Scheduler started. Sending daily email at {send_time} every day.")

    send_daily_news()

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()