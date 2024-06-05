from utils.helpers.index import url_insert_bulk
from utils.slack import detailed_error_slack_message

from .helper import (
    COMPETITOR,
    MAX_COUNT,
    get_manufacturer_page_links,
    get_product_links_from_plp,
)


def get_products_urls_and_store(product_list_page_link):
    products_links_outputs = []
    count = 0
    is_next_page_available = True

    try:
        while is_next_page_available:
            try:
                product_links, next_page = get_product_links_from_plp(product_list_page_link)
                print(
                    "page results: ",
                    len(product_links),
                    " next page: ",
                    next_page,
                    " for: ",
                    product_list_page_link,
                    " count: ",
                    count,
                )
                if product_links:
                    for product_link in product_links:
                        count += 1
                        result = {
                            "competitor": COMPETITOR,
                            "url": product_link,
                            "scraper_type": "live_search",
                            "from_manufacturer": True,
                        }
                        products_links_outputs.append(result)

                if next_page:
                    product_list_page_link = next_page
                else:
                    is_next_page_available = False

                if count >= MAX_COUNT:
                    url_insert_bulk(products_links_outputs)
                    products_links_outputs = []
                    count = 0
            except Exception as e:
                detailed_error_slack_message(e, COMPETITOR)
                continue

        if count > 0:
            url_insert_bulk(products_links_outputs)
            products_links_outputs = []
            count = 0
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)

    if len(products_links_outputs) > 0:
        url_insert_bulk(products_links_outputs)


def get_and_store_wolf_automation_urls():
    try:
        manufacturer_page_links = get_manufacturer_page_links()

        for manufacturer_page_link in manufacturer_page_links:
            get_products_urls_and_store(manufacturer_page_link)

    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
