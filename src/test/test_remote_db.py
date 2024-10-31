import os
import unittest
import sys
from db.remote_tweets_db import TweetsDB
from hijri_year_progress import HijriYearProgress
from datetime import datetime
from dotenv import load_dotenv
from db.models.tweet import Tweet
from logger import *

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
        today_hijri_year_progress = HijriYearProgress(
            date_time=datetime(month=8, year=2024, day=12))
        # new tweet object
        tweet = Tweet(hijri_year=today_hijri_year_progress.year, percent=int(
            today_hijri_year_progress.percent), post_id="1851780441683968057", post_link="https://x.com/user/status/1851053064347701666")
        # format the new generated to test it
        new_tweet = tweet.format_to_insert_in_db()
        # insert the new tweet
        tweet_row = tweetsDB.insert_new_tweet(tweet)
        # format the new inserted tweet in the db to test it
        tweet_row = Tweet.format_dic_to_json(tweet_row)
        # testing
        self.assertEqual(new_tweet, tweet_row)

    def test_length_of_tweets_rows(self):
        # instanciate a db client with the remote database
        tweetsDB = TweetsDB(url=url, key=key)

        data = tweetsDB.get_all_tweets()

        size = len(data)

        self.assertEqual(11, size)


if __name__ == '__main__':
    # Load specific tests only
    suite = unittest.TestSuite()
    # suite.addTest(TestRemoteDB('test_length_of_tweets_rows'))
    suite.addTest(TestRemoteDB('test_insert_new_tweet'))

    # Run only the selected tests
    runner = unittest.TextTestRunner()
    runner.run(suite)
