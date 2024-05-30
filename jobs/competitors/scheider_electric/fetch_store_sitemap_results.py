from utils.helpers.index import url_insert_bulk, get_sitemap_urls
from utils.slack import error_slack_message

COMPETITOR = "scheiderelectric"
URL = "https://www.se.com/us/en/product/google-product-sitemapindex-US-en.xml"
MAX_COUNT = 5000


def get_and_store_scheiderElectric_urls():
    try:
        outputs = []
        sitemap_url = get_sitemap_urls(URL, COMPETITOR)
        for data in sitemap_url:
            sitemap_url_data = get_sitemap_urls(data, COMPETITOR)
            for i in sitemap_url_data:
                result = {"competitor": COMPETITOR, "url": i, "scraper_type": "sitemap"}
                outputs.append(result)
                if len(outputs) == MAX_COUNT:
                    url_insert_bulk(outputs)
                    outputs = []
        if outputs and len(outputs):
            url_insert_bulk(outputs)
    except Exception as e:
        error_slack_message(e)
