import traceback
import uuid

from services.mssql.connection import get_mssql_connection
from utils.slack import send_slack_message


def insert_cron_job_start_status(job_title):
    try:
        connection = get_mssql_connection()
        cursor = connection.cursor()
        cursor.execute("BEGIN TRANSACTION")
        status = "Active"
        job_id = uuid.uuid4()
        insert_cronjob_logs_query = f"""INSERT INTO cron_job_histories
        (id, job_title, status, start_time, created_at, updated_at)
        VALUES
        (
            '{job_id}',
            '{job_title}',
            '{status}',
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        )"""
        send_slack_message("Running insertion query for cron_job logs")
        cursor.execute(insert_cronjob_logs_query)
        cursor.execute("COMMIT TRANSACTION")
        connection.commit()
        return job_id
    except Exception as e:
        message = "Error: " + str(e) + "\n" + traceback.format_exc()
        send_slack_message(message, "error")


def update_cron_job_completed_status(job_title, job_id, status="Completed"):
    try:
        connection = get_mssql_connection()
        cursor = connection.cursor()
        cursor.execute("BEGIN TRANSACTION")
        update_cronjob_logs_query = f"""UPDATE cron_job_histories SET
            job_title = '{job_title}',
            status = '{status}',
            end_time = CURRENT_TIMESTAMP,
            updated_at = CURRENT_TIMESTAMP
            WHERE id = '{job_id}'"""
        cursor.execute(update_cronjob_logs_query)
        send_slack_message(f"Running update query for cron_job logs with status: {status}")
        cursor.execute("COMMIT TRANSACTION")
        connection.commit()
    except Exception as e:
        message = "Error: " + str(e) + "\n" + traceback.format_exc()
        send_slack_message(message, "error")


def competitors_only_for_algo_query():
    try:
        connection = get_mssql_connection()
        cursor = connection.cursor()
        query = f"""SELECT name from competitors WHERE consider_for_pricing_algo = 1 AND status != 'red' or status IS NULL"""  # noqa: F541
        cursor.execute(query)
        competitors_only_for_algo = cursor.fetchall()
        competitors_only_for_algo = [item[0] for item in competitors_only_for_algo]
        return competitors_only_for_algo
    except Exception as e:
        message = "Error: " + str(e) + "\n" + traceback.format_exc()
        send_slack_message(message, "error")
