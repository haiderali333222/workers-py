import requests

from bs4 import BeautifulSoup

from utils.helpers.index  import url_insert_bulk, error_slack_message
from services.slack.slack_message import send_slack_message


COMPETITOR = 'relectric'
URL = 'https://www.relectric.com/content/sitemap/products-index.xml'


def get_and_store_relectric_urls():
    try:
        page = requests.get(URL)
        if page.status_code != 200:
            message = "Error: "+COMPETITOR + page.text
            send_slack_message(message)
        sitemap_index = BeautifulSoup(page.content, 'html.parser')
        urls = [element.text for element in sitemap_index.findAll('loc')]
        for data in urls:
            output = requests.get(data)
            sitemap_url = BeautifulSoup(output.content, 'html.parser')
            output_result = [
                output.text for output in sitemap_url.findAll('loc')]
            outputs = []
            for i in output_result:
                result = {
                    "competitor": COMPETITOR,
                    "url": i,
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
