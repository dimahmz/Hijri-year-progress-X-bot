from dotenv import load_dotenv
import os
import tweepy


load_dotenv("src/.env.local")

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_KEY_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")



def main ():
    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )
    response = client.create_tweet(
        text="hello world"
    )
    print(f"https://twitter.com/user/status/{response.data['id']}")


if __name__ == "__main__":
    main()