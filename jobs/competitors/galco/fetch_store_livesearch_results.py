from .helper import get_manufacturer_page_links,get_products_urls_and_store
from utils.helpers.index import error_slack_message, error_slack_message
from utils.slack import send_slack_message

COMPETITOR = 'galco'
MANUFACTURERS_URL = 'https://www.galco.com/manufacturers'
BASE_URL = 'https://www.galco.com'
PAGE_LIMIT = 25


def get_and_store_galco_urls():
    try:
        message = f"start getting url for {COMPETITOR}"
        send_slack_message(message)

        manufacturer_page_links = get_manufacturer_page_links() 
        for manufacturer_page_link in manufacturer_page_links:
            get_products_urls_and_store(manufacturer_page_link)

        message = f"end getting url for {COMPETITOR}"
        send_slack_message(message)

    except Exception as e:
        error_slack_message(e)