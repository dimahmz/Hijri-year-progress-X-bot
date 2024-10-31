from dotenv import load_dotenv
import os
import tweepy
from hijri_year_progress import HijriYearProgress
from datetime import datetime
from logger import *
from db.models.tweet import Tweet
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

    if (is_allowed == False):
        debug_logger.debug(f"The bot is not allowed to tweet hijri_year_progress : {
                           hijri_year_progress}")
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
            wait_on_rate_limit=True
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

        url = f"https://x.com/user/status/{post_id}"

        # new tweet object
        new_tweet = Tweet(post_id=post_id, post_link=url, percent=int(
            hijri_year_progress.percent), hijri_year=hijri_year_progress.year)

        tweetsDB = TweetsDB(url=url, key=key)
        # store the tweet in a remote database
        new_tweet_row = tweetsDB.insert_new_tweet(new_tweet)

        # log to ensure everything is working
        info_logger.info(f""" A new tweet has been posted at : {
            datetime.now()} : link : {url}: tweet : {new_tweet_row}""")

        return True

    except Exception as e:
        # logging the error
        error_logger.error(f"An error has occurred {e}")
        # @TODO : send the admin a message
        return False



if __name__ == "__main__":
    print("The bot is trying to tweet")
    main()
