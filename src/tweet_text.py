from hijri_year_progress import HijriYearProgress

# tweet some info about the year progress
def teweet_text_generator(hijriYearProgress  : HijriYearProgress) -> str:
    # teweet lines
    tweet_lines = ["{0}{1}{2}{3}{4}".format(
        "مضى", f" %{int(hijriYearProgress.percent)} ", "من", f" {hijriYearProgress.year} ","هجري"),]
    tweet_text = "\n".join(tweet_lines)
    return tweet_text

