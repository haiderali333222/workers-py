from bs4 import BeautifulSoup

from config.index import API_KEY_SCRAPY
from utils.helpers.index import download_gz_file, get_proxies, request_with_retry
from utils.slack import detailed_error_slack_message

from .read_gz import store_data

MAX_RETRIES = 5
URL = "https://www.plchardware.com/sitemap/sitemaps.xml"
COMPETITOR = "plchardware"


def get_and_store_plchardware_urls():
    try:
        scraper_api_url = f"https://api.scraperapi.com/?api_key={API_KEY_SCRAPY}&url={URL}&ultra_premium=true"

        proxies, headers = get_proxies()
        page = request_with_retry(
            "get",
            scraper_api_url,
            proxies=proxies,
            headers=headers,
            retries=MAX_RETRIES,
        )

        sitemap_index = BeautifulSoup(page.content, "html.parser")
        sitemap_url = [element.text for element in sitemap_index.findAll("loc")]
        count = 0
        for data in sitemap_url:
            if "product" in data:
                count += 1
                path = download_gz_file("plchardware", data, count, ultra_premium=True)
                store_data(path)
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
