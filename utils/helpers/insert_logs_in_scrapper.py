import traceback

from services.mssql.connection import get_mssql_connection
from services.slack.slack_message import send_slack_message


def insert_logs_in_scrapper_competitor_using_query(query_params):
    try:
        connection = get_mssql_connection()
        cursor = connection.cursor()
        cursor.execute("BEGIN TRANSACTION")
        insert_logs_query = f"""INSERT INTO scraper_competitor_logs
        (id, scrapers, start_time, created_by, created_at, updated_at, scraper_type)
        VALUES
        (
            '{query_params["id"]}',
            '["{query_params["scrapers"]}"]',
            CURRENT_TIMESTAMP,
            '{query_params["created_by"]}',
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP,
            '{query_params["scraper_type"]}'
        )
        """
        send_slack_message("Running insertion query for logs")
        cursor.execute(insert_logs_query)
        cursor.execute("COMMIT TRANSACTION")
        connection.commit()
    except Exception as e:
        message = "Error: " + str(e) + "\n" + traceback.format_exc()
        send_slack_message(message)
