from hijri_year_progress import HijriYearProgress
from db.remote_tweets_db import TweetsDB
from dotenv import load_dotenv
import os


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
    except:
        # database in empty
        # an error in my code
        return False

    # should not tweet the same percentage twice
    if (percent == int(new_hijri_year_progress.percent)):
        return False

    # I don't know what error may cause this happen
    if (percent > int(new_hijri_year_progress.percent)):
        return False

    # percent > int(new_hijri_year_progress.percent)
    return True
