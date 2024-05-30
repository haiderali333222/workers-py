from bs4 import BeautifulSoup
from utils.helpers.index import url_insert_bulk, request_with_retry, get_proxies, error_slack_message
from utils.slack import send_slack_message

COMPETITOR = 'globaltestsupply'
URL = 'https://www.globaltestsupply.com/sitemap.xml'


def get_and_store_globaltestsupply_urls():
    try:
        # page = requests.get(url)
        proxies, headers = get_proxies()
        page = request_with_retry(
            "get", URL, COMPETITOR, proxies=proxies, headers=headers)
        outputs = []
        if page.status_code != 200:
            message = f"Error: {COMPETITOR} {page.text}"
            send_slack_message(message)
        sitemap_index = BeautifulSoup(page.content, 'html.parser')
        sitemap_url = [
            element.text for element in sitemap_index.findAll('loc')]
        for data in sitemap_url:
            proxies, headers = get_proxies()
            page_data = request_with_retry(
                "get", data, COMPETITOR, proxies=proxies, headers=headers)
            if page_data.status_code != 200:
                message = f"Error: {COMPETITOR}{page.text}"
                send_slack_message(message)
            data_sitemap_index = BeautifulSoup(
                page_data.content, 'html.parser')
            data_sitemap_url = [
                element.text for element in data_sitemap_index.findAll('loc')]
            for output in data_sitemap_url:
                result = {
                    "competitor": COMPETITOR,
                    "url": output,
                    "scraper_type": "sitemap"
                }
                outputs.append(result)
                if len(outputs) == 5000:
                    url_insert_bulk(outputs)
                    outputs = []
            if outputs and len(outputs):
                url_insert_bulk(outputs)
    except Exception as e:
        error_slack_message(e)
