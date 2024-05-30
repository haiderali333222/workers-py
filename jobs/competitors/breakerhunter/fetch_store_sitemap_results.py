import requests
from bs4 import BeautifulSoup
from utils.helpers.index import url_insert_bulk, error_slack_message
from utils.slack import send_slack_message


COMPETITOR = "breakerhunter"
URL = 'https://breakerhunters.com/sitemap.xml'


def get_and_store_breakerhunters_urls():
    try:
        page = requests.get(URL)
        if page.status_code != 200:
            message = f"Error: {COMPETITOR} {page.text}"
            send_slack_message(message)
        sitemap_index = BeautifulSoup(page.content, 'html.parser')
        urls = [element.text for element in sitemap_index.findAll('loc')]
        outputs = []
        for data in urls:
            if 'sitemap_products' in data:
                sitemap = requests.get(data)
                result_index = BeautifulSoup(sitemap.content, 'html.parser')
                for element in result_index.findAll('loc'):
                    if '/products' in element.text:
                        result = {
                            "competitor": COMPETITOR,
                            "url": element.text,
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
