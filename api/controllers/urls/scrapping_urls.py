import traceback
from concurrent.futures import ThreadPoolExecutor
from mapping.mapping_for_urls import URLS
from utils.slack import send_slack_message

FUTURES = []

def multithreaded_url_scraper(competitors):
    try:
        global FUTURES
        executor = ThreadPoolExecutor(len(competitors))
        for competitor in competitors:
            if competitor in URLS.keys():
                future = executor.submit(URLS[competitor])
                FUTURES.append(future)
    except Exception as e:
        message = f"Error: {str(e)}" + "\n" + traceback.format_exc()
        send_slack_message(message)