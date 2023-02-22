import schedule
import time
from rss_main import task_for_schedule

schedule.every().day.at('00:00').do(task_for_schedule)
while True:
    schedule.run_pending()
    time.sleep(1)
