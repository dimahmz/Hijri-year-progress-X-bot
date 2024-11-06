from dataclasses import dataclass
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Log:
    id: int = 0
    message: str = ""
    pathname: int = 0
    lineno: int = 1
    logged_at: datetime = datetime.now().isoformat()
    created_at: datetime = datetime.now().isoformat()

    def format_to_insert_in_db(self):
        log = {
            "message": self.message,
            "pathname": self.pathname,
            "lineno": self.lineno,
            "logged_at": self.logged_at,
        }
        return log

    @staticmethod
    def format_dic_to_json(tweet):
        log = {
            "message": tweet["message"],
            "pathname": tweet["pathname"],
            "lineno": tweet["lineno"],
            "logged_at": tweet["logged_at"],
        }
        return log
