from utils.helpers.index import error_slack_message
from .helper import (
    get_manufacturer_page_links,
    get_products_urls_and_store,
    COMPETITOR,
)
from utils.slack import detailed_error_slack_message


def get_and_store_galco_urls():
    try:
        manufacturer_page_links = get_manufacturer_page_links()
        for manufacturer_page_link in manufacturer_page_links:
            get_products_urls_and_store(manufacturer_page_link)
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
