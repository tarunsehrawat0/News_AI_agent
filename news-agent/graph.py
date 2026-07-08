from langgraph.graph import END, START, StateGraph

from email_sender import send_email
from state import State
from tools import fetch_latest_india_news, summarize_article, today_string


def fetch_news_node(state: State) -> dict:
    return {"articles": fetch_latest_india_news()}


def summarize_news_node(state: State) -> dict:
    summaries = []
    for article in state.get("articles", []):
        summaries.append(summarize_article(article))
    return {"summaries": summaries}


def create_email_node(state: State) -> dict:
    lines = [f"Daily AI News Digest - {today_string()}", ""]
    articles = state.get("articles", [])
    summaries = state.get("summaries", [])

    for index, article in enumerate(articles):
        summary = summaries[index] if index < len(summaries) else "No summary available."
        lines.append(f"{index + 1}. {article.get('title', 'Untitled article')}")
        lines.append(summary)
        lines.append(f"Link: {article.get('url', '')}")
        lines.append("")

    return {"email": "\n".join(lines).strip()}


def send_email_node(state: State) -> dict:
    subject = f"Daily AI News Digest - {today_string()}"
    send_email(subject=subject, body=state.get("email", ""))
    return {}


def build_graph():
    graph = StateGraph(State)
    graph.add_node("fetch_news", fetch_news_node)
    graph.add_node("summarize_news", summarize_news_node)
    graph.add_node("create_email", create_email_node)
    graph.add_node("send_email", send_email_node)

    graph.add_edge(START, "fetch_news")
    graph.add_edge("fetch_news", "summarize_news")
    graph.add_edge("summarize_news", "create_email")
    graph.add_edge("create_email", "send_email")
    graph.add_edge("send_email", END)
    return graph.compile()


app = build_graph()
