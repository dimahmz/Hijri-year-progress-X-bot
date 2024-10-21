from datetime import datetime
from hijridate import Gregorian


class HijriYearProgress:
    total_days: int
    left_days: int
    year: int
    percent: float
    completed_days: int

    def __init__(self, date_time : datetime = None):
        # using the current date as a default date
        if(date_time==None) : 
            date_time = datetime.now()

        # convert a The current date into Hijri
        current_hijri_date = Gregorian(
            date_time.year, date_time.month, date_time.day).to_hijri()
        # print(f"current_hijri_date: {current_hijri_date}")

        # get how many days in this hijri year
        days_of_current_hijri_year = current_hijri_date.year_length()
        # print(f"\n days_of_current_hijri_year : {days_of_current_hijri_year}")

        # Calculate the number of days completed from the start of the year
        # I assummed that there is 30 days in each month but this is incorrect
        # @TODO : find a way to get the number of days in each month in this Hijri year
        completed_days = (current_hijri_date.month - 1) * \
            30 + current_hijri_date.day
        
        self.total_days = days_of_current_hijri_year
        self.left_days = days_of_current_hijri_year - completed_days
        self.year = current_hijri_date.year
        self.percent = (completed_days / days_of_current_hijri_year)*100
        self.completed_days = completed_days
    
    def __str__(self):
        return f"total_days: {self.total_days}, left_days: {self.left_days}, year: {self.year}, percent: {self.percent}, completed_days: {self.completed_days}"