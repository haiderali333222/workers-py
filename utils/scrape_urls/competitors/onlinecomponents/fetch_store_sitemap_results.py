from utils.helpers.index import (
    get_sitemap_urls,
    preprocess_manufacturers,
    url_insert_bulk,
)
from utils.slack import detailed_error_slack_message

from .helper import is_manufacturer_match, is_valid_url_and_manufacturer

COMPETITOR = "onlinecomponents"
STARTING_URL = "https://www.onlinecomponents.com/sitemaps.xml"


def get_and_store_online_components_urls():
    try:
        manufacturers_dict = preprocess_manufacturers()
        count = 0
        outputs = []
        limit = 5000

        sitemap_urls = get_sitemap_urls(STARTING_URL, COMPETITOR)

        print(f"Found {len(sitemap_urls)} sitemap urls")

        for sitemap_url in sitemap_urls:
            website_urls = get_sitemap_urls(sitemap_url, COMPETITOR)

            for url in website_urls:
                is_valid, manufacturer = is_valid_url_and_manufacturer(url)

                if is_valid and manufacturer and is_manufacturer_match(manufacturers_dict, manufacturer):
                    count += 1
                    result = {
                        "competitor": COMPETITOR,
                        "url": url,
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
