from .sql_db import sqlDB
from .models.tweet import Tweet
from typing import Final


class TweetsDB:

    dbname: Final = "tweets.db"

    @staticmethod
    def newTweetPosted(tweet: Tweet):
        tweets_db = sqlDB(TweetsDB.dbname)
        cursor = tweets_db.connection.cursor()
        create_table_query = """
          CREATE TABLE IF NOT EXISTS tweets (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              post_id TEXT NOT NULL,
              post_link TEXT NOT NULL,
              progress_percent INTEGER NOT NULL,
              posted_at DATE NOT NULL,
              created_at DATE DEFAULT (DATE('now'))
          );
        """
        cursor.execute(create_table_query)

        data = [
            (tweet.post_id, tweet.post_link, tweet.progress_percent,
             tweet.posted_at, tweet.created_at)
        ]

        cursor.executemany(
            "INSERT INTO tweets (post_id, post_link, progress_percent, posted_at, created_at) VALUES(?,?,?,?,?)", data)

        tweets_db.connection.commit()

        tweets_db.closeConnection()

    @staticmethod
    def get_percent_in_last_tweet() -> int:
        # this may fail
        # connect to the database
        tweets_db = sqlDB(TweetsDB.dbname)
        conn = tweets_db.connection

        cursor = conn.cursor()

        # SQL query to select all rows from the tweets table
        select_query = "SELECT progress_percent FROM tweets ORDER BY created_at DESC LIMIT 1"

        try:
            # execute the query
            cursor.execute(select_query)
        except Exception:
            # table doesn't exist yet
            return 0
        
        # fetch all rows
        progress_percent = cursor.fetchone()

        # databse is empty
        if(progress_percent==None):  return 0

        # close the connection
        tweets_db.closeConnection()

        return progress_percent[0]

    @staticmethod
    def get_all_tweets():
        # connect to the database
        tweets_db = sqlDB(TweetsDB.dbname)
        conn = tweets_db.connection

        cursor = conn.cursor()

        # SQL query to select all rows from the tweets table
        select_query = "SELECT * FROM tweets"

        # execute the query
        cursor.execute(select_query)

        # fetch all rows
        rows = cursor.fetchall()

        # close the connection
        tweets_db.closeConnection()

        return rows

    @staticmethod
    def update_tweets_table(query: str):
        tweets_db = sqlDB(TweetsDB.dbname)

        conn = tweets_db.connection
        conn.execute(query)

        conn.commit()

        tweets_db.closeConnection()
