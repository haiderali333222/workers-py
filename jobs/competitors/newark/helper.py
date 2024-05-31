from utils.helpers.index import (
    check_manufacturer_match,
    preprocess_manufacturers,
    get_page_with_scraperapi_from_url,
)
from utils.slack import detailed_error_slack_message

COMPETITOR = "newark"
MANUFACTURERS_URL = "https://www.newark.com/manufacturers"
BASE_URL = "https://www.newark.com"
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
        return False


def get_manufacturer_page_links():
    manufacturer_page_links = []

    try:
        manufacturers_dict = preprocess_manufacturers()
        if manufacturer_page := get_page_with_scraperapi_from_url(
            MANUFACTURERS_URL, COMPETITOR
        ):
            mfr_groups = manufacturer_page.find_all("div", class_="manuSection")
            for mfr_group in mfr_groups:
                manf_lists = mfr_group.find_all("li")
                for manf_links in manf_lists:
                    if link := manf_links.find("a"):
                        if href := link["href"]:
                            manf_name = href.split("/")[-1]
                            if is_manufacturer_match(manufacturers_dict, manf_name):
                                matched_manufacturer_link = (
                                    f"{BASE_URL}/w/search/prl/results?brand={manf_name}"
                                )
                                manufacturer_page_links.append(
                                    matched_manufacturer_link
                                )
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)

    return manufacturer_page_links


def get_product_links_from_plp(plp_link, is_first_page=False):
    product_links = []
    next_page_links = []

    try:
        manf_name = plp_link.split("=")[-1]
        plp_page = get_page_with_scraperapi_from_url(plp_link, COMPETITOR)
        product_table = plp_page.find("table", class_="productLister")

        if product_table:
            table_rows = product_table.find_all("tr")
            for rows in table_rows:
                tds = rows.find("td", class_="description")
                if tds:
                    link = tds.find("a")
                    if link:
                        href = link["href"]
                        product_links.append(href)

        if is_first_page:
            if total_results := plp_page.find("span", id="titleProdCount"):
                total_results = total_results.text.strip().replace(",", "")
                print("total result... ", total_results)
                if int(total_results) > PAGE_LIMIT:
                    total_pages = int(total_results) // PAGE_LIMIT
                    for i in range(2, total_pages + 2):
                        next_page_link = f"https://www.newark.com/search/prl/results/{i}?brand={manf_name}"
                        next_page_links.append(next_page_link)
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)

    return product_links, next_page_links


def add_product_links_to_outputs(product_links):
    product_links_outputs = []

    if product_links:
        for product_link in product_links:
            result = {
                "competitor": COMPETITOR,
                "url": product_link,
                "scraper_type": "live_search",
                "from_manufacturer": True,
            }
            product_links_outputs.append(result)

    return product_links_outputs
