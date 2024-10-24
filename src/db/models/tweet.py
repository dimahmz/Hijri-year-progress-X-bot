from dataclasses import dataclass
from datetime import date

@dataclass
class Tweet:
    post_id: int = 0
    post_link: str = ""
    progress_percent: int =""
    posted_at: date = date.today()
    created_at: date = date.today()

