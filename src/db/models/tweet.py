from dataclasses import dataclass
from datetime import datetime
from dataclasses import dataclass, asdict
import json


@dataclass
class Tweet:
    id: int = 0
    post_id: str = "0"
    post_link: str = ""
    percent: int = 0
    hijri_year: int = 1
    posted_at: datetime = datetime.now().isoformat()
    created_at: datetime = datetime.now().isoformat()

    def format_to_insert_in_db(self):

        tweet = {
            "post_id": self.post_id,
            "post_link": self.post_link,
            "percent": self.percent,
            "hijri_year": self.hijri_year,
            "posted_at": self.posted_at

        }
        return tweet

    @staticmethod
    def format_dic_to_json(tweet):
        tweet = {
            "post_id": tweet["post_id"],
            "post_link": tweet["post_link"],
            "percent": tweet["percent"],
            "hijri_year": tweet["hijri_year"],
            "posted_at": tweet["posted_at"]
        }
        return tweet
