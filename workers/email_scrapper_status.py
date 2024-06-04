from config.index import DB_NAME, ENVIRONMENT
from services.celery.celery_app import celery_app
from services.email.send_email import email
from utils.slack import send_slack_message
from utils.constants import SEND_SCRAPERS_STATUS_EMAIL_RECIPIENT_TO, SEND_SCRAPERS_STATUS_EMAIL_RECIPIENT_CC, SEND_SCRAPERS_STATUS_EMAIL_SUBJECT
from celery_once import QueueOnce  # prevents multiple execution and queuing of celery tasks
from utils.constants import scraper_status_email_body_template
from datetime import datetime, timedelta
from services.mongo_db.connection import mongoConnection
from utils.cronjob_logs import insert_cron_job_start_status, update_cron_job_completed_status
from scripts.competitor_url_fix import competitor_url_fix
from scripts.remove_competitor_duplicate import remove_duplicate_for_all_competitor
from scripts.send_scraped_data_summary import scraped_data_summary
# from rungoogleshoppingurls import runGoogleShoppingURLs

db = mongoConnection()[DB_NAME]

@celery_app.task(base=QueueOnce, once={'graceful': True})
def run_tasks():
    try:
        JOB_TITTLE = 'scraper-logs-status'
        job_id = insert_cron_job_start_status(JOB_TITTLE)
        send_scrapper_status()
        send_slack_message("start: send summary scrape")
        # runGoogleShoppingURLs()
        scraped_data_summary()
        # # competitor_url_fix()
        send_slack_message("done: send summary scrape")
        # remove_duplicate_for_all_competitor()
        update_cron_job_completed_status(JOB_TITTLE, job_id)
    except Exception as e:
        send_slack_message(f"Error while executing job: {e}")
        update_cron_job_completed_status(JOB_TITTLE, job_id, status = 'Error')
    
def send_scrapper_status():
    try:
        send_slack_message("Job to send scrappers status via email started") 
        working_payload = {}
        not_working_payload = {}
        eight_days_ago = datetime.now() - timedelta(days=288)
        db_error_logs = db.error_logs.find(
            {
                "capture_at": {
                "$gte": eight_days_ago,
            },
            },
        )
        last_week_entries = list(db_error_logs)
        for entry in last_week_entries:
            chance = (entry['total'] / 100) * 10
            if (
                entry['total'] > 100
                and entry['errors'] > entry['success']
                and entry['errors'] > chance
            ):  
                not_working_payload[entry['competitor']]= {'success': entry['success'], 'error': entry['errors']}
            elif entry['success'] > entry['errors']:
                working_payload[entry['competitor']]= {'success': entry['success'], 'error': entry['errors']}

        for key in working_payload:
            not_working_payload.pop(key, None)
        print(working_payload,not_working_payload)
        SCRAPER_STATUS = scraper_status_email_body_template(working_payload,not_working_payload)
        send_slack_message("Amplify Scraper Status emails being send now")
        email_subject = SEND_SCRAPERS_STATUS_EMAIL_SUBJECT  
        if ENVIRONMENT == "staging":
            email_subject += " -Staging"
        email(SCRAPER_STATUS, SEND_SCRAPERS_STATUS_EMAIL_RECIPIENT_TO, email_subject, SEND_SCRAPERS_STATUS_EMAIL_RECIPIENT_CC)
    except Exception as e:
        send_slack_message(f"Error while executing job: {e}")
send_scrapper_status()