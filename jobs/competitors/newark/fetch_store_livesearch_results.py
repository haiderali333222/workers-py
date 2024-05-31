from utils.helpers.index import url_insert_bulk
from utils.slack import detailed_error_slack_message
from .helper import (
    get_manufacturer_page_links,
    get_product_links_from_plp,
    MAX_COUNT,
    add_product_links_to_outputs,
    COMPETITOR,
)


def get_products_urls_and_store(product_list_page_link):
    products_links_outputs = []
    try:
        product_links, next_pages = get_product_links_from_plp(
            product_list_page_link, is_first_page=True
        )

        print(
            f"product_links: {len(product_links)} and next_pages: {len(next_pages)} for {product_list_page_link}, current count: {len(products_links_outputs)}"
        )

        if product_links:
            first_page_links = add_product_links_to_outputs(product_links)
            products_links_outputs.extend(first_page_links)

        for next_page in next_pages:
            try:
                next_page_product_links, _ = get_product_links_from_plp(next_page)

                if next_page_product_links:
                    found_links = add_product_links_to_outputs(next_page_product_links)
                    products_links_outputs.extend(found_links)

                if len(products_links_outputs) >= MAX_COUNT:
                    url_insert_bulk(products_links_outputs)
                    products_links_outputs = []
            except Exception as e:
                detailed_error_slack_message(e, COMPETITOR)
                continue

        if len(products_links_outputs) > 0:
            url_insert_bulk(products_links_outputs)
            products_links_outputs = []
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
    if len(products_links_outputs) > 0:
        url_insert_bulk(products_links_outputs)


def get_and_store_newark_urls():
    try:
        manufacturer_page_links = get_manufacturer_page_links()
        print(f"matched manufacturers: {len(manufacturer_page_links)}")
        for manufacturer_page_link in manufacturer_page_links:
            get_products_urls_and_store(manufacturer_page_link)

    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
