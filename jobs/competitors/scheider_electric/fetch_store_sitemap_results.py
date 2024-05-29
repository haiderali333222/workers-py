import requests

from bs4 import BeautifulSoup

from utils.helpers.index  import url_insert_bulk, error_slack_message
from services.slack.slack_message import send_slack_message

COMPETITOR = 'scheiderElectric'
URL = 'https://www.se.com/us/en/product/google-product-sitemapindex-US-en.xml'


def get_and_store_scheiderElectric_urls():
    try:
        outputs = []
        page = requests.get(URL)
        if page.status_code != 200:
            message = "Error: "+COMPETITOR + page.text
            send_slack_message(message)
        sitemap_index = BeautifulSoup(page.content, 'html.parser')
        sitemap_url = [
            element.text for element in sitemap_index.findAll('loc')]
        for data in sitemap_url:
            data = data.strip()
            page_data = requests.get(data)
            sitemap_index_data = BeautifulSoup(
                page_data.content, 'html.parser')
            sitemap_url_data = [
                element.text for element in sitemap_index_data.findAll('loc')]
            for i in sitemap_url_data:
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
