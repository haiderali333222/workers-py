from utils.helpers.index import download_gz_file, get_sitemap_urls
from utils.slack import detailed_error_slack_message
from config.index import API_KEY_SCRAPY

from .helper import store_data

COMPETITOR = "us.rs-online"
URL = "https://us.rs-online.com/sitemap.xml"


def get_and_store_rs_urls():
    try:
        scrape_api = f"https://api.scraperapi.com/?api_key={API_KEY_SCRAPY}&url={URL}&country_code=us"
        sitemaps_urls = get_sitemap_urls(scrape_api, COMPETITOR)
        for count, url in enumerate(sitemaps_urls, start=1):
            path = download_gz_file(COMPETITOR, url, count)
            print(f"Downloaded {path}")
            store_data(path)
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
