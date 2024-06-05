import concurrent.futures

from utils.es.executor import extracted_name, total_count
from utils.slack import detailed_error_slack_message

from .helper import COMPETITOR, creating_url

count = 0


def get_and_store_breakeroutlet_urls():
    try:
        increment_value = 5000
        total_products = total_count()
        i = 0
        executor = concurrent.futures.ThreadPoolExecutor(10)
        while i < total_products:
            mydb_col_output = extracted_name(i, increment_value)
            i = i + increment_value
            for data in mydb_col_output:
                executor.submit(creating_url, data)
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
