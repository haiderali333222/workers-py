from utils.helpers.index import url_insert_bulk, get_sitemap_urls
from utils.slack import error_slack_message

COMPETITOR = "iesupply"
URL = "https://www.iesupply.com/sitemaps/sitemap-products-0.xml"
MAX_COUNT = 5000


def get_and_store_iesupplyy_urls():
    try:
        outputs = []
        sitemap_url = get_sitemap_urls(URL, COMPETITOR)
        for data in sitemap_url:
            if "product" in data:
                result = {
                    "competitor": COMPETITOR,
                    "url": data,
                    "scraper_type": "sitemap",
                }
                outputs.append(result)
                if len(outputs) == MAX_COUNT:
                    url_insert_bulk(outputs)
                    outputs = []
        if outputs and len(outputs):
            url_insert_bulk(outputs)
    except Exception as e:
        error_slack_message(e)
