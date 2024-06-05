import concurrent.futures

from .helper import creating_url, COMPETITOR
from utils.es.executor import total_count, extracted_name
from utils.slack import detailed_error_slack_message


def get_and_store_coasttocoastbreaker_urls():
    try:
        increment_value = 5000
        total_products = total_count()
        i = 0
        executor = concurrent.futures.ThreadPoolExecutor(20)
        while i < total_products:
            mydb_col_output = extracted_name(i, increment_value)
            i += increment_value
            for data in mydb_col_output:
                executor.submit(creating_url, data)
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
