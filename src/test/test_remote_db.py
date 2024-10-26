import os
import unittest
import sys
from db.remote_tweets_db import TweetsDB
from hijri_year_progress import HijriYearProgress
from datetime import datetime
from dotenv import load_dotenv
from db.models.tweet import Tweet
from dataclasses import asdict

sys.path.insert(0, '..')

load_dotenv(".env.test")
# db credentials for testing env 
url = os.getenv("TEST_SUPABASE_URL")
key = os.getenv("TEST_SUPABASE_KEY")

class TestRemoteDB(unittest.TestCase):
    # normal insertion
    def test_insert_new_tweet(self):
        # instanciate a db client with the remote database
        tweetsDB = TweetsDB(url=url, key=key)
        # create a test case
        today_hijri_year_progress = HijriYearProgress(date_time=datetime.now())
        # new tweet object
        tweet = Tweet(hijri_year=today_hijri_year_progress.year, percent=int(
            today_hijri_year_progress.percent), post_id="0000", post_link="x.com/hijri_tracke")
        # format the new generated to test it 
        new_tweet = tweet.format_to_test()
        # insert the new tweet
        tweet_row = tweetsDB.insert_new_tweet(tweet)
        # format the new inserted tweet in the db to test it
        tweet_row = Tweet.format_dic_to_test(tweet_row)
        # testing
        self.assertEqual(new_tweet, tweet_row)


if __name__ == '__main__':
    unittest.main()
