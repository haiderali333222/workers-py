from utils.helpers.index import (
    check_manufacturer_match,
    preprocess_manufacturers,
    get_page_with_scraperapi_from_url,
)
from utils.slack import send_slack_message

COMPETITOR = "mouser"
MANUFACTURERS_URL = "https://eu.mouser.com/manufacturer/"
BASE_URL = "https://eu.mouser.com"
MAX_COUNT = 5000
manufacturers_match_status = {}


def is_manufacturer_match(manufacturers_dict, product_title):
    try:
        is_calculated = manufacturers_match_status.get(product_title)

        if is_calculated is not None:
            return is_calculated

        is_match = check_manufacturer_match(manufacturers_dict, product_title)
        manufacturers_match_status[product_title] = is_match

        return is_match
    except Exception as e:
        send_slack_message(e)
        return False


def get_manufacturer_page_links():
    manufacturer_page_links = []
    try:
        manufacturers_dict = preprocess_manufacturers()
        if manufacturer_page := get_page_with_scraperapi_from_url(
            MANUFACTURERS_URL, COMPETITOR, is_ultra_premium=True
        ):
            if mfr_list := manufacturer_page.find("div", id="mfr_list"):
                mfr_groups = mfr_list.find_all("div", class_="mfr_group")
                for mfr_group in mfr_groups:
                    mfrs = mfr_group.find_all("li")
                    for mfr in mfrs:
                        if a := mfr.find("a"):
                            href = a["href"]

                            if href and "/manufacturer" in href:
                                if manf_name := href.replace("/manufacturer/", ""):
                                    if is_manufacturer_match(
                                        manufacturers_dict, manf_name
                                    ):
                                        matched_manufacturer_link = f"{BASE_URL}{href}"

                                        manufacturer_page_links.append(
                                            matched_manufacturer_link
                                        )
    except Exception as e:
        send_slack_message(e)

    return manufacturer_page_links


def get_product_links_from_plp(plp_link):
    product_links = []
    next_page_link = None
    try:
        if plp_page := get_page_with_scraperapi_from_url(
            plp_link, COMPETITOR, is_ultra_premium=True
        ):
            if product_link_tags := plp_page.find_all("div", class_="mfr-part-num"):
                for product_link_tag in product_link_tags:
                    if a := product_link_tag.find("a"):
                        product_links.append(f"{BASE_URL}{a['href']}")

            if next_page_tag := plp_page.find("a", id="lnkPager_lnkNext"):
                if next_page_link_href := next_page_tag["href"]:
                    if BASE_URL not in next_page_link_href:
                        next_page_link_href = f"{BASE_URL}{next_page_link_href}"

                    next_page_link = next_page_link_href.strip()

        return product_links, next_page_link
    except Exception as e:
        send_slack_message(e)
        return product_links, next_page_link
