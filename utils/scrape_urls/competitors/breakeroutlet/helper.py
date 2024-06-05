from bs4 import BeautifulSoup

from utils.helpers.index import get_proxies, request_with_retry, url_insert_bulk
from utils.slack import detailed_error_slack_message, send_slack_message

COMPETITOR = "breakeroutlet"
URL = "https://breakeroutlet.com/search.php?search_query="


def creating_url(name):
    try:
        url_formed = URL
        url_formed += name
        store_breakerout(url_formed)
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)


def store_breakerout(url_formed):
    outputs = []
    proxies, headers = get_proxies()
    response = request_with_retry("get", url_formed, COMPETITOR, proxies=proxies, headers=headers)
    if response.status_code != 200:
        message = f"Error:  {COMPETITOR} {response.text}"
        send_slack_message(message, "error")
    soup = BeautifulSoup(response.content, "html5lib")
    products_details = soup.find("div", attrs={"id": "product-listing-container"})
    products_details_info = products_details.find("form", attrs={"class": "both-grid-default"})
    product_ul = products_details_info.find("ul", attrs={"class": "productGrid visible"})
    for a in product_ul.find_all("li", attrs={"class": "product"}):
        result = {
            "competitor": COMPETITOR,
            "url": (a.find("a")["href"]),
            "scraper_type": "live_search",
        }
        outputs.append(result)
    if outputs and len(outputs):
        url_insert_bulk(outputs)
