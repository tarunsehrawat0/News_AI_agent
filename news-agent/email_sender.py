import os
import re
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(address: str | None) -> bool:
    return bool(address and EMAIL_PATTERN.match(address))


def send_email(subject: str, body: str, is_html: bool = False) -> None:
    """Send an email through Gmail SMTP using an app password."""
    gmail_user = os.getenv("GMAIL_USER")
    gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")
    to_email = os.getenv("TO_EMAIL", gmail_user)

    if not gmail_user or not gmail_app_password:
        raise ValueError("Missing GMAIL_USER or GMAIL_APP_PASSWORD in .env")
    if not to_email:
        raise ValueError("Missing TO_EMAIL in .env")
    if not is_valid_email(gmail_user):
        raise ValueError("GMAIL_USER is not a valid email address")
    if not is_valid_email(to_email):
        raise ValueError("TO_EMAIL is not a valid email address")

    message = MIMEText(body, "html" if is_html else "plain", "utf-8")
    message["Subject"] = subject
    message["From"] = gmail_user
    message["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(gmail_user, gmail_app_password)
        server.sendmail(gmail_user, [to_email], message.as_string())
