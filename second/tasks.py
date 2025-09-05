from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from .services import save_parking_basic, save_parking_availability
from django_apscheduler.models import DjangoJob

scheduler = None


def start():
    global scheduler
    if scheduler is not None:
        return  # 이미 시작했으면 종료

    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    try:
        existing_jobs = DjangoJob.objects.filter(id__in=['basic_job', 'availability_job'])
        for job in existing_jobs:
            job.delete()
    except DjangoJob.DoesNotExist:
        pass

    # 기본정보: 하루 1회
    # scheduler.add_job(save_parking_basic, 'cron', hour=2, minute=0, id='basic_job', replace_existing=True, next_run_time=datetime.now())

    # 가용정보: 5분마다
    # scheduler.add_job(save_parking_availability, 'interval', minutes=1, id='availability_job', replace_existing=True)

    scheduler.start()
