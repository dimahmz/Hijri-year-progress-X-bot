from hijri_year_progress import HijriYearProgress
from db.tweets_db import TweetsDB


def allow_the_bot_to_tweet(new_hijri_year_progress: HijriYearProgress) -> bool:
    try:
        # get the last tweet
        percent = TweetsDB.get_percent_in_last_tweet()
    except:
        # database in empty
        # an error in my code
        return False

    # should not tweet the same percentage twice
    if (percent == int(new_hijri_year_progress.percent)):
        return False
    
    # I don't know what error may cause this happen
    if (percent > int(new_hijri_year_progress.percent)):
        return False
    
    # percent > int(new_hijri_year_progress.percent)
    return True
