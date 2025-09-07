from hijri_year_progress import HijriYearProgress
from db.remote_tweets_db import TweetsDB
from db.models.log import Log
from dotenv import load_dotenv
import os
import inspect

relative_path = os.path.relpath(__file__)

load_dotenv(".env")

environment = os.getenv("ENVIRONMENT")
prefix = ""

# load test environment if the bot isn't in production mode
if (environment != "production"):
    load_dotenv(".env.test")
    prefix = "TEST_"

url = os.getenv(f"{prefix}SUPABASE_URL")
key = os.getenv(f"{prefix}SUPABASE_KEY")


def allow_the_bot_to_tweet(new_hijri_year_progress: HijriYearProgress, tweets_db: TweetsDB = None) -> bool:
    try:
        # production use
        if (tweets_db == None):
            tweets_db = TweetsDB(key=key, url=url)
        # get the last tweet
        percent = tweets_db.get_percent_in_last_tweet()
        hijri_year = tweets_db.get_year_in_last_tweet()
    except Exception as e:
        line_number = inspect.currentframe().f_lineno
        log = Log(message=e, pathname=relative_path, lineno=line_number)

        tweets_db.log_to_remote_db(type="error", log=log)
        # database in empty
        # an error in my code
        # log in the console
        print("Error occurred check logs")
        return False
    
    # the year has changed, so we can tweet
    if(new_hijri_year_progress.hijri_year > hijri_year):
        return True

    # should not tweet the same percentage twice
    if (percent == int(new_hijri_year_progress.percent)):
        return False

    # I don't know what error may cause this happen
    if (percent > int(new_hijri_year_progress.percent)):
        return False

    # percent > int(new_hijri_year_progress.percent)
    return True
