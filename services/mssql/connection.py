import pymssql

from config.index import MSDB_NAME, PASSWORD, SERVER_NAME, USER_NAME
from utils.slack import send_slack_message

mssql_connection = None


def get_mssql_connection():
    global mssql_connection

    if mssql_connection is None:
        mssql_connection = pymssql.connect(server=SERVER_NAME, user=USER_NAME, password=PASSWORD, database=MSDB_NAME)
        send_slack_message("New connection created for mssql")
    else:
        send_slack_message("Connection already exists for mssql")

    return mssql_connection
