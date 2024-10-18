from dotenv import load_dotenv
from datetime import datetime
from hijridate import Gregorian
import os
import tweepy


load_dotenv("src/.env.local")

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_KEY_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")


def hijri_year_progress_percent():
    # get the current datetime
    today_datetime = datetime.now()

    # convert a The current date into Hijri
    current_hijri_date = Gregorian(
        today_datetime.year, today_datetime.month, today_datetime.day).to_hijri()
    # print(f"current_hijri_date: {current_hijri_date}")

    # get how many days in this hijri year
    days_of_current_hijri_year = current_hijri_date.year_length()
    # print(f"\n days_of_current_hijri_year : {days_of_current_hijri_year}")

    # Calculate the number of days completed from the start of the year
    # I assummed that there is 30 days in each month but this is incorrect
    # @TODO : find a way to get the number of days in each month in this Hijri year
    days_completed = (current_hijri_date.month - 1) * \
        30 + current_hijri_date.day
    # print(f"days_completed : {days_completed}")

    # the perecent of the completed days in the current hijri year
    percent = days_completed / days_of_current_hijri_year
    return f"days_of_current_hijri_year : {days_of_current_hijri_year} \ndays_completed :{days_completed} \npercent {percent*100}"


def main ():
    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )
    percent_text = hijri_year_progress_percent()
    response = client.create_tweet(
        text=percent_text
    )
    print(f"https://twitter.com/user/status/{response.data['id']}")


if __name__ == "__main__":
    main()