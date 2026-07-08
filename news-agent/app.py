from graph import app


def run_news_agent() -> str:
    """Run the LangGraph workflow once and return the generated email text."""
    initial_state = {"articles": [], "summaries": [], "email": ""}
    result = app.invoke(initial_state)
    return result.get("email", "")


if __name__ == "__main__":
    email_text = run_news_agent()
    print("Email sent successfully.")
    print(email_text)
