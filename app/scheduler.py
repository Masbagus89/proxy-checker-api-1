from apscheduler.schedulers.background import BackgroundScheduler
from app.checker import run_proxy_check

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(run_proxy_check, 'interval', hours=1, id="auto_checker")
    scheduler.start()
