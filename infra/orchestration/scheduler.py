# scheduler.py
"""
Sample scheduler script for orchestration (e.g., APScheduler).
"""
from apscheduler.schedulers.background import BackgroundScheduler

def scheduled_job():
    print("Scheduled job executed.")

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_job, 'interval', seconds=10)
    scheduler.start()
    print("Scheduler started. Press Ctrl+C to exit.")
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
