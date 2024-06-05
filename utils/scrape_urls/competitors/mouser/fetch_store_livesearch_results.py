from utils.helpers.index import (
    url_insert_bulk,
)
from utils.slack import detailed_error_slack_message
from .helper import (
    BASE_URL,
    COMPETITOR,
    get_manufacturer_page_links,
    get_page_with_scraperapi_from_url,
    get_product_links_from_plp,
    MAX_COUNT,
)

manufacturers_match_status = {}


def get_manufacturer_products_links(manufacturer_page_link):
    products_links_outputs = []
    count = 0
    try:
        if manufacture_page := get_page_with_scraperapi_from_url(
            manufacturer_page_link, COMPETITOR, is_ultra_premium=True
        ):
            if all_products_div := manufacture_page.find(
                "div", class_="all_products"
            ):
                if link_input := all_products_div.find("input"):
                    plp_link = f"{BASE_URL}{link_input['value']}"
                    next_page_exists = True
                    print(f"plp_link: {plp_link}")

                    while next_page_exists:
                        product_links, next_page = get_product_links_from_plp(
                            plp_link
                        )
                        print(
                            f"product_links: {len(product_links)} next_page: {next_page} count: {count}"
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
                            plp_link = next_page
                        else:
                            next_page_exists = False

                        if count >= MAX_COUNT:
                            url_insert_bulk(products_links_outputs)
                            products_links_outputs = []
                            count = 0

                    if count > 0:
                        url_insert_bulk(products_links_outputs)
                        products_links_outputs = []
                        count = 0
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
    if len(products_links_outputs) > 0:
        url_insert_bulk(products_links_outputs)


def get_and_store_mouser_urls():
    try:
        manufacturer_page_links = get_manufacturer_page_links()

        for manufacturer_page_link in manufacturer_page_links:
            get_manufacturer_products_links(manufacturer_page_link)

    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
