from hijri_year_progress import HijriYearProgress
from db.remote_tweets_db import TweetsDB


def allow_the_bot_to_tweet(new_hijri_year_progress: HijriYearProgress, tweets_db : TweetsDB =None) -> bool:
    try:
        #production use
        if(tweets_db==None) :
            tweets_db = TweetsDB()
        # get the last tweet
        percent = tweets_db.get_percent_in_last_tweet()
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
