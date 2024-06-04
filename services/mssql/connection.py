import pymssql
from services.slack.slack_message import send_slack_message
from config.index import SERVER_NAME, MSDB_NAME, USER_NAME, PASSWORD

mssql_connection = None


def get_mssql_connection():
    global mssql_connection

    if mssql_connection is None:
        mssql_connection = pymssql.connect(server=SERVER_NAME, user=USER_NAME, password=PASSWORD, database=MSDB_NAME)
        send_slack_message("New connection created for mssql")
        return mssql_connection
    else:
        send_slack_message("Connection already exists for mssql")
        return mssql_connection
