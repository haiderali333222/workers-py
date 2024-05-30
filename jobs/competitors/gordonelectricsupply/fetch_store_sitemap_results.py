from utils.helpers.index import error_slack_message, download_gz_file, get_sitemap_urls
from config.index import API_KEY_SCRAPY

from .helper import *

COMPETITOR = "gordonelectricsupply"
URL = "https://www.gordonelectricsupply.com/sitemap-index.xml"


def get_and_store_gordonelectricsupply_urls():
    try:
        scrape_api = f"https://api.scraperapi.com/?api_key={API_KEY_SCRAPY}&url={URL}&ultra_premium=true"
        sitemap_urls = get_sitemap_urls(scrape_api, COMPETITOR)
        for count, data in enumerate(sitemap_urls, start=1):
            path = download_gz_file(COMPETITOR, data, count, ultra_premium=True)
            store_data(path)
    except Exception as e:
        error_slack_message(e)
