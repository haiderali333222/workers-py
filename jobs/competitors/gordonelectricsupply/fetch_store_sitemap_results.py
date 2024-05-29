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

        message = "start getting url for "+ COMPETITOR
        send_slack_message(message)
        # proxies, headers = get_proxies()
        # page = request_with_retry(
        #     "get", URL, COMPETITOR, proxies=proxies, headers=headers)
        if page.status_code != 200:
            message = "Error: "+COMPETITOR + page.text
            send_slack_message(message)
        sitemap_index = BeautifulSoup(page.content, 'html.parser')
        sitemap_url = [
            element.text for element in sitemap_index.findAll('loc')]
        count = 0
        for data in sitemap_url:
            count += 1
            download_gz_file(COMPETITOR, data, count)
            store_data("sitemap-"+COMPETITOR+str(count)+".xml.gz")
    except Exception as e:
        error_slack_message(e)
