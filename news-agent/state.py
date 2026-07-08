from typing import List, TypedDict


class State(TypedDict):
    articles: List[dict]
    summaries: List[str]
    email: str
