import schedule
import time
import random

def run_job():
    # we introduce a random delay of 1 to 120 minutes to avoid overloading the server
    _sleep = random
    print(f'Sleeping for {_sleep} seconds')
    time.sleep(_sleep)

    from main import main
    print(f'Running main() now at {time.strftime("%H:%M:%S", time.localtime())}')
    main()

schedule.every().day.at("08:00").do(run_job)