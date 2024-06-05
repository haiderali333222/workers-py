import concurrent.futures
import traceback

from bs4 import BeautifulSoup

from utils.es.executor import extracted_name, total_count
from utils.helpers.index import get_proxies, request_with_retry, url_insert_bulk
from utils.slack import send_slack_message

count = 0
url = "https://www.radwell.co.uk"


def radwell_url():
    increment_value = 5000
    total_products = total_count()
    i = 0
    executor = concurrent.futures.ThreadPoolExecutor(20)
    while i < total_products:
        mydb_col_output = extracted_name(i, increment_value)
        i = i + increment_value
        for data in mydb_col_output:
            executor.submit(creating_url, data)


def store_radwell(url_formed):
    outputs = []
    proxies, headers = get_proxies()
    response = request_with_retry("get", url_formed, "radwell", proxies=proxies, headers=headers)

    if response.status_code != 200:
        message = "Error: radwell " + response.text
        send_slack_message(message, "error")
        return
    soup = BeautifulSoup(response.content, "html5lib")
    products_details = soup.find("div", attrs={"id": "searchResults"})
    if products_details is None:
        return
    products_details_info = products_details.find_all("div", attrs={"class": "searchResult clickable"})
    for a in products_details_info:
        data = a.find("a")["href"]
        data = url + data
        if "Buy" in data:
            result = {
                "competitor": "radwell",
                "url": data,
                "scraper_type": "live_search",
            }
            outputs.append(result)
    if outputs and len(outputs):
        url_insert_bulk(outputs)
    return True


def creating_url(name):
    try:
        url_formed = url
        url_formed += "/en-GB/Search?PartNumber=" + name + "&SearchMethod=starts&PageSize=5"
        store_radwell(url_formed)
    except Exception as e:
        message = "Error: " + str(e) + "\n" + traceback.format_exc()
        send_slack_message(message, "error")
