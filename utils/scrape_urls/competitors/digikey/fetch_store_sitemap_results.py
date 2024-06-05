from config.index import API_KEY_SCRAPY
from utils.helpers.index import (
    get_sitemap_urls,
    preprocess_manufacturers,
    url_insert_bulk,
)
from utils.slack import detailed_error_slack_message

from .helper import extract_manufacturer_from_url, is_manufacturer_match

COMPETITOR = "digikey"
URL = "https://www.digikey.com/product-detail/sitemap.xml"
scrappy_api_url = f"https://api.scraperapi.com/?api_key={API_KEY_SCRAPY}&ultra_premium=true"


def get_and_store_digikey_urls():
    try:
        manufacturers_dict = preprocess_manufacturers()
        count = 0
        outputs = []
        limit = 5000

        sitemap_scrape_api_url = f"{scrappy_api_url}&url={URL}&country_code=us"
        sitemap_urls = get_sitemap_urls(sitemap_scrape_api_url, COMPETITOR)

        for url in sitemap_urls:
            next_sitemap_url = f"{scrappy_api_url}&url={url}&country_code=us"
            next_sitemap_urls = get_sitemap_urls(next_sitemap_url, COMPETITOR)

            for next_url in next_sitemap_urls:
                manufacturer, is_valid = extract_manufacturer_from_url(next_url)
                if is_valid and manufacturer and is_manufacturer_match(manufacturers_dict, manufacturer):
                    count += 1
                    result = {
                        "competitor": COMPETITOR,
                        "url": next_url,
                        "scraper_type": "sitemap",
                        "from_manufacturer": True,
                    }
                    outputs.append(result)
                    if count >= limit:
                        url_insert_bulk(outputs)
                        count = 0
                        outputs = []

        if outputs and len(outputs):
            url_insert_bulk(outputs)
            outputs = []

    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
