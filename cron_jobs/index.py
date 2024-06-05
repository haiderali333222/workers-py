from celery.schedules import crontab

cron_jobs = {
    "celery_job": {
        "weekly_job_for_scrapper_status": {
            "task": "scrapper_scheduler.tasks.email_scrapper_status.run_tasks",
            "schedule": crontab(minute=0, hour=10),
            "options": {"queue": "celery_queue_for_send_scrapper_status"},
        }
    }
}
