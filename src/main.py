from dotenv import load_dotenv
import os
import tweepy
from hijri_year_progress import HijriYearProgress
from datetime import datetime
from logger import *
from db.models.tweet import Tweet
from db.models.log import Log
from db.remote_tweets_db import TweetsDB
from tweet_text import teweet_text_generator
from progress_bar import generate_progress_bar
from decider import allow_the_bot_to_tweet


def main():
    # environment set up
    load_dotenv(".env")
    environment = os.getenv("ENVIRONMENT")
    prefix = ""

    # load test environment if the bot isn't in production
    if (environment != "production"):
        load_dotenv(".env.test")
        prefix = "TEST_"

    # environment variables
    consumer_key = os.getenv(f"{prefix}CONSUMER_KEY")
    consumer_secret = os.getenv(f"{prefix}CONSUMER_KEY_SECRET")
    access_token = os.getenv(f"{prefix}ACCESS_TOKEN")
    access_token_secret = os.getenv(f"{prefix}ACCESS_TOKEN_SECRET")
    bearer_token = os.getenv(f"{prefix}bearer_token")
    url = os.getenv(f"{prefix}SUPABASE_URL")
    key = os.getenv(f"{prefix}SUPABASE_KEY")

    # instanciate a new hijri year progress
    hijri_year_progress = HijriYearProgress()

    # decide whether the bot can tweet or not
    is_allowed = allow_the_bot_to_tweet(hijri_year_progress)

    # TODO:
    # what if this throw an error
    tweetsDB = TweetsDB(url=url, key=key)

    if (is_allowed == False):
        # debug message
        message = f"The bot is not allowed to tweet hijri_year_progress : {hijri_year_progress}"
        # log locally
        debug_logger.debug(message)
        # log remotely
        log = Log(pathname="src/main.py", lineno=51, logged_at=datetime.now().isoformat(), message=message)
        tweetsDB.log_to_remote_db(type="debug", log=log)
        return False

    # generate a new tweet for the that hijri year
    tweet_text = teweet_text_generator(hijri_year_progress)

    try:
        # V1 Twitter API Authentication
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)

        # V2 Twitter API Authentication
        client = tweepy.Client(
            bearer_token,
            consumer_key, consumer_secret,
            access_token, access_token_secret,
            wait_on_rate_limit=False
        )

        # generate a progress image bar the that hijri year
        filename = generate_progress_bar(hijri_year_progress.percent)

        media_id = api.media_upload(filename).media_id_string

        
        # create the tweet
        response = client.create_tweet(
            text=tweet_text,
            media_ids=[media_id]
        )

        post_id = response.data['id']

        post_link = f"https://x.com/user/status/{post_id}"

        # new tweet object
        new_tweet = Tweet(hijri_year=hijri_year_progress.year, percent=int(
            hijri_year_progress.percent), post_id=post_id, post_link=post_link)

        # store the tweet in a remote database
        new_tweet_row = tweetsDB.insert_new_tweet(new_tweet)

        message  = f"A new tweet has been posted at : {datetime.now()} : new_tweet : {new_tweet_row}"

        # log to ensure everything is working
        info_logger.info(message)

        # close db connection
        log = Log(pathname="src/main.py", lineno=96, logged_at=datetime.now().isoformat(), message=message)

        tweetsDB.log_to_remote_db(type="info", log=log)

        return True

    except Exception as e:
        # logging the error
        error_message = f"An error has occurred {e}"
        error_logger.error(error_message)
        log = Log(pathname="src/main.py", lineno=106, logged_at=datetime.now().isoformat(), message=error_message)
        tweetsDB.log_to_remote_db(type="error", log=log)

        # @TODO : send the admin a message
        return False
    finally:
        # close db connection
        tweetsDB.close_db_connection()


if __name__ == "__main__":
    print("The bot is trying to tweet")
    main()
    print("Finished execution")
