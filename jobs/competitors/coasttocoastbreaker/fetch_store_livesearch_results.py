import concurrent.futures

from .helper import creating_url
from utils.helpers.index import error_slack_message
from utils.es.executor import total_count, extracted_name



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
        error_slack_message(e)