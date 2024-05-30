import requests

from bs4 import BeautifulSoup

from utils.helpers.index  import url_insert_bulk, error_slack_message
from services.slack.slack_message import send_slack_message

COMPETITOR = 'imcdirect'
URL = 'https://www.imc-direct.com/sitemap.xml'


def get_and_store_imcdirect_urls():
    try:
        outputs = []
        page = requests.get(URL)
        if page.status_code != 200:
            message = f"Error: {COMPETITOR}{page.text}"
            send_slack_message(message)
        sitemap_index = BeautifulSoup(page.content, 'html.parser')
        sitemap_url = [
            element.text for element in sitemap_index.findAll('loc')]
        for data in sitemap_url:
            result = {
                "competitor": COMPETITOR,
                "url": data,
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
