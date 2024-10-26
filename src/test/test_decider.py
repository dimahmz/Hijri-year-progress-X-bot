import unittest
from decider import allow_the_bot_to_tweet
from hijri_year_progress import HijriYearProgress
from datetime import datetime
from db.remote_tweets_db import TweetsDB
import sys
from dotenv import load_dotenv
import os
sys.path.insert(0, '..')


load_dotenv(".env.test")
# db credentials for testing env
url = os.getenv("TEST_SUPABASE_URL")
key = os.getenv("TEST_SUPABASE_KEY")
tweetsDB = TweetsDB(url, key)


class TestDeciderMethods(unittest.TestCase):

    def test_1_decider_result(self):
        today_hijri_year_progress = HijriYearProgress(date_time=datetime.now())
        self.assertEqual(False, allow_the_bot_to_tweet(
            today_hijri_year_progress, tweetsDB))

    def test_2_decider_result(self):
        last_month_hijri_year_progress = HijriYearProgress(
            date_time=datetime(year=2024, month=9, day=1))
        self.assertEqual(False, allow_the_bot_to_tweet(
            last_month_hijri_year_progress, tweetsDB))

    def test_3_decider_result(self):
        next_month_hijri_year_progress = HijriYearProgress(
            date_time=datetime(year=2024, month=11, day=1))
        self.assertEqual(True, allow_the_bot_to_tweet(
            next_month_hijri_year_progress, tweetsDB))

    def test_4_decider_result(self):
        yesterday_month_hijri_year_progress = HijriYearProgress(
            date_time=datetime(year=2024, month=10, day=22))
        self.assertEqual(False, allow_the_bot_to_tweet(
            yesterday_month_hijri_year_progress, tweetsDB))


if __name__ == '__main__':
    unittest.main()
