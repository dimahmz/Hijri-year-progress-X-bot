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
    def format_str_to_test(new_log : str):
        log = {
            "message": new_log["message"],
            "pathname": new_log["pathname"],
            "lineno": new_log["lineno"],
            "logged_at": new_log["logged_at"],
        }
        return log

    def format_to_test(self):
        log = {
            "message": self.message,
            "pathname": self.pathname,
            "lineno": self.lineno,
            "logged_at": self.logged_at,
        }
        return log
