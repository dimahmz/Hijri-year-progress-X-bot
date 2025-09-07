from supabase import create_client, Client, ClientOptions
from db.models.tweet import Tweet
from db.models.log import Log
from logger import *
from typing import Literal


class TweetsDB:
    supabase: Client
    
    def __init__(self, url: str, key: str):
        self.supabase = create_client(
            url, key, options=ClientOptions(auto_refresh_token=False))

    def get_all_tweets(self):
        response = self.supabase.table("tweets").select("*").execute()
        return response.data

    # insert a new tweet into a remote database
    def insert_new_tweet(self, tweet: Tweet):
        try:
            tweet = tweet.format_to_insert_in_db()
            response = (self.supabase.table("tweets").insert(tweet).execute())
            return response.data[0]

        except Exception as e:
            # TODO: this should not fail
            error_logger.error(
                f"error when inserting the new tweet in the database : {e}")
            return False

    def get_percent_in_last_tweet(self):
        response = self.supabase.table("tweets").select(
            "*").order("created_at", desc=True).limit(1).execute()
        # TODO:
        # error cases to handle :
        # server error
        # table doesn't exist

        # table is empty
        if (len(response.data) == 0):
            return 0

        return response.data[0]["percent"]

    def get_year_in_last_tweet(self):
        response = self.supabase.table("tweets").select(
            "*").order("created_at", desc=True).limit(1).execute()
        # TODO:
        # error cases to handle :
        # server error
        # table doesn't exist

        # table is empty
        if (len(response.data) == 0):
            return 0

        return response.data[0]["hijri_year"]

    def log_to_remote_db(self, type: Literal["error", "info", "debug", "warning"], log: Log):
        # TODO:
        # handle errors
        try : 
            log = log.format_to_insert_in_db()
            table_name = f"{type}s"
            # plural exception 
            if(type=="info"):
                table_name = type
            response = (self.supabase.table(table_name).insert(log).execute())
            return response.data[0]
        except Exception as e:
            print(e)
            return False
 
    def close_db_connection(self):
        self.supabase.auth.sign_out()
