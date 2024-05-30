import time
import requests

from config.index import API_KEY_SCRAPY
from utils.slack import send_slack_message, error_slack_message
from utils.helpers.index import get_proxies, request_with_retry

from .read_gz import *

MAX_RETRIES = 5
URL = 'https://www.plchardware.com/sitemap/sitemaps.xml'


def download_gz(url, count, chunk_size=125000):
    retries = 0
    scraper_api_url = f'https://api.scraperapi.com/?api_key={API_KEY_SCRAPY}&url={url}'

    while retries < MAX_RETRIES:
        response = requests.get(scraper_api_url)
        if response.status_code == 200:
            break
        retries += 1
        time.sleep(2)
    open(f"sitemap-plchardware{str(count)}.xml.gz", "wb").write(response.content)


def get_and_store_plchardware_urls():
    try:
        scraper_api_url = f'https://api.scraperapi.com/?api_key={API_KEY_SCRAPY}&url={URL}'

        proxies, headers = get_proxies()
        page = request_with_retry("get", scraper_api_url, proxies=proxies, headers=headers, retries=MAX_RETRIES)

        sitemap_index = BeautifulSoup(page.content, 'html.parser')
        sitemap_url = [element.text for element in sitemap_index.findAll('loc')]
        count = 0
        for data in sitemap_url:
            if 'product' in data:
                count += 1
                download_gz(data, count)
                store_data(f"sitemap-plchardware{count}.xml.gz")
    except Exception as e:
        error_slack_message(e)