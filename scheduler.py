import schedule
import time
from datetime import datetime
from scrapper import scrape_data

def job():
    print("Starting the scraping job...")
    scrape_data()
    print("Scraping job completed.")

def monthly_job():
    today = datetime.today()
    # Check if today is the first day of the month
    if today.day == 1:
        job()

def yearly_job():
    today = datetime.today()
    # Check if today is January 1st
    if today.month == 1 and today.day == 1:
        job()

# Schedule daily and weekly jobs
schedule.every().day.at("00:00").do(job)  # Run daily at midnight
schedule.every().week.do(job)            # Run weekly

# Custom scheduling for monthly and yearly jobs
def custom_scheduler():
    while True:
        # Check and run monthly job
        monthly_job()
        # Check and run yearly job
        yearly_job()
        # Run every second
        time.sleep(1)

# Start the scheduler
custom_scheduler()
