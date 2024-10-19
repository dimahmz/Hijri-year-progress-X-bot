from dotenv import load_dotenv
from datetime import datetime
from hijridate import Gregorian
import os
import tweepy
from typing import TypedDict


class YearProgressPayload(TypedDict):
    total_days: int
    completed_days: int
    left_days: int
    year: int
    percent: int


load_dotenv("src/.env.local")

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_KEY_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

completed_bar_char = "█"
incompleted_bar_char = "░"
progress_bar_total_chars = 27


def hijri_year_progress():
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

    # returns the current hijri year days and the completed days
    hijri_year_progress_payload: YearProgressPayload = {
        "total_days": days_of_current_hijri_year,
        "completed_days": days_completed,
        "left_days": days_of_current_hijri_year - days_completed,
        "year": current_hijri_date.year,
        "percent": int((days_completed / days_of_current_hijri_year)*100)
    }
    return hijri_year_progress_payload

# return the progress bar


def progress_bar_genrator(total: int, completed: int) -> str:
    # happens one time
    if (total == completed):
        return "[" + completed_bar_char * progress_bar_total_chars + "]"

    # calculate chars' multipliers
    completed_percent = completed/total
    completed_multiplier = progress_bar_total_chars * completed_percent
    incompleted_multiplier = progress_bar_total_chars - completed_multiplier

    # chars of the progress bar
    completed_section = completed_bar_char * int(completed_multiplier)
    incompleted_section = incompleted_bar_char * int(incompleted_multiplier)

    # the progress bar
    progress_bar = "║{0}{1}║".format(completed_section, incompleted_section)

    return progress_bar


def teweet_text() -> str:
    # payload for the the current year progress
    year_progress_payload: YearProgressPayload = hijri_year_progress()
    # progress bar as a text
    progress_bar = progress_bar_genrator(
        year_progress_payload["total_days"], year_progress_payload["completed_days"])
    # teweet lines
    tweet_lines = [
        f"السنة الهجرية {year_progress_payload["year"]}",
        f"\n{progress_bar}",
        f"\n% {year_progress_payload["percent"]} مكتمل",
        f"{year_progress_payload["left_days"]} يوم متبقي",
    ]
    tweet_text = "\n".join(tweet_lines)
    return tweet_text


def main():
    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )
    response = client.create_tweet(
        text=teweet_text()
    )
    print(f"https://twitter.com/user/status/{response.data['id']}")


if __name__ == "__main__":
    main()
