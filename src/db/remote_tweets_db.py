from supabase import create_client, Client
from dotenv import load_dotenv
import os
from datetime import datetime
from db.models.tweet import Tweet


class TweetsDB:
    supabase: Client

    def __init__(self, url: str = None, key: str = None):
        try :
            url = url
            key = key
            if (url == None or key == None):
                load_dotenv(".env")
                url = os.getenv("SUPABASE_URL")
                key = os.getenv("SUPABASE_KEY")
            self.supabase = create_client(url, key)
        except :
            raise("couldn't instanciate the supabase client")
        
    def get_all_tweets(self):
        response = self.supabase.table("tweets").select("*").execute()
        return response.data

    def insert_new_tweet(self, tweet: Tweet):
        response = (self.supabase.table("tweets").insert(
            {"post_id": tweet.post_id, "post_link": tweet.post_link, "percent": tweet.percent, "posted_at": tweet.posted_at, "hijri_year": tweet.hijri_year}).execute())
        return response.data[0]

    def get_percent_in_last_tweet(self):
        response = self.supabase.table("tweets").select(
            "*").order("created_at", desc=True).limit(1).execute()
        # TODO: error cases to handle
        # server error 

        # table doesn't exist

        # table is empty
        if(len(response.data)==0) : return 0

        return response.data[0]["percent"]

tweetsDb = TweetsDB()
