from utils.helpers.index import (
    check_manufacturer_match,
    get_page_from_url,
    preprocess_manufacturers,
)
from utils.slack import detailed_error_slack_message

COMPETITOR = "wolfautomation"
MANUFACTURERS_URL = "https://www.wolfautomation.com/brands"
BASE_URL = "https://www.wolfautomation.com"
PAGE_LIMIT = 25
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
        detailed_error_slack_message(e, COMPETITOR)


def get_manufacturer_page_links():
    manufacturers_dict = preprocess_manufacturers()
    url_to_parse_manufacturer = MANUFACTURERS_URL
    manufacturer_page_links = []

    try:
        while url_to_parse_manufacturer:
            if manufacturer_page := get_page_from_url(url_to_parse_manufacturer, COMPETITOR):
                manufacturer_group_wrapper = manufacturer_page.find("div", class_="ob-subcategory-carousel")
                if manufacturer_groups := manufacturer_group_wrapper.find_all("div", class_="subcat-box"):
                    for manufacturer_group in manufacturer_groups:
                        if a := manufacturer_group.find("a"):
                            href = a["href"]
                            if href and "/brands" in href:
                                if manf_name := href.split("/brands")[-1]:
                                    if is_manufacturer_match(manufacturers_dict, manf_name):
                                        matched_manufacturer_link = f"{href}?limit=99"
                                        manufacturer_page_links.append(matched_manufacturer_link)

                if next_page := manufacturer_page.find("li", class_="pagination-item pagination-item--next"):
                    if a := next_page.find("a"):
                        url = a["href"]
                        url_to_parse_manufacturer = f"{BASE_URL}{url}" if BASE_URL not in url else url
                else:
                    url_to_parse_manufacturer = None
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)

    return manufacturer_page_links


def get_product_links_from_plp(plp_link):
    product_links = []
    next_page_link = None

    try:
        plp_page = get_page_from_url(plp_link, COMPETITOR)
        if product_link_tags := plp_page.find_all("li", class_="product"):
            for product_link_tag in product_link_tags:
                if a := product_link_tag.find("a", class_="card-figure__link"):
                    if "href" in a.attrs:
                        product_href = a["href"]
                        if BASE_URL not in product_href:
                            product_href = f"{BASE_URL}{product_href}"
                        else:
                            product_href = product_href.strip()
                        product_links.append(product_href)

        if next_page_tag := plp_page.find("li", class_="pagination-item pagination-item--next"):
            if next_page_tag:
                if a := next_page_tag.find("a"):
                    if "href" in a.attrs:
                        next_page_link = a["href"]
                        if BASE_URL not in next_page_link:
                            next_page_link = f"{BASE_URL}{next_page_link}"
                        else:
                            next_page_link = next_page_link.strip()
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)

    return product_links, next_page_link
