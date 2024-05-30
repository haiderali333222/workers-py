import requests
from bs4 import BeautifulSoup

from utils.helpers.index import error_slack_message, download_gz_file
from .helper import *
from services.slack.slack_message import send_slack_message

from config.index import API_KEY_SCRAPY


COMPETITOR = 'gordonelectricsupply'
URL = 'https://www.gordonelectricsupply.com/sitemap-index.xml'


def get_and_store_gordonelectricsupply_urls():
    try:
        scrape_api = f'https://api.scraperapi.com/?api_key={API_KEY_SCRAPY}&url={URL}'
        page = requests.get(scrape_api)

        if page.status_code != 200:
            message = f"Error: {COMPETITOR} {page.text}"
            send_slack_message(message)
        sitemap_index = BeautifulSoup(page.content, 'html.parser')
        sitemap_url = [
            element.text for element in sitemap_index.findAll('loc')]
        for count, data in enumerate(sitemap_url, start=1):
            path = download_gz_file(COMPETITOR, data, count)
            store_data(path)
    except Exception as e:
        error_slack_message(e)
