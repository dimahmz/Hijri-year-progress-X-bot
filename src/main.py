from dotenv import load_dotenv
import os
import tweepy
from hijri_year_progress import HijriYearProgress
from datetime import datetime
from logger import *
from db.models.tweet import Tweet
from datetime import date
from db.remote_tweets_db import TweetsDB
from tweet_text import teweet_text_generator
from progress_bar import generate_progress_bar
from decider import allow_the_bot_to_tweet
import time


load_dotenv(".env")

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_KEY_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("bearer_token")


def main():
    # instanciate a new hijri year progress
    hijri_year_progress = HijriYearProgress()

    # decide whether the bot can tweet or not
    is_allowed = allow_the_bot_to_tweet(hijri_year_progress)

    if (is_allowed == False):
        debug_logger.debug(f"The bot is not allowed to tweet hijri_year_progress : {hijri_year_progress}")
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

        new_tweet = Tweet(post_id=post_id,post_link=url, progress_percent=int(
            hijri_year_progress.percent), posted_at=date.today(), hijri_year=hijri_year_progress.year)

        # store the tweet in a remote database
        TweetsDB.insert_new_tweet(new_tweet)
        
        # log to ensure everything is working
        info_logger.info(f""" a new tweet has been posted at : {
                    datetime.now()} : link : {url}: tweet : {new_tweet}""")

        return True

    except Exception as e:
        # logging the error
        error_logger.error(f"an error has occured {e}")
        # @TODO : send the admin a message
        return False



if __name__ == "__main__":
    print("App has been started")
    info_logger.info("App has been started")
    one_hour = 60*60
    iteration = 0
    while True:
        iteration+=1
        print(f"iterating number : {iteration}")
        main()
        time.sleep(one_hour)
