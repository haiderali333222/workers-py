from utils.helpers.index import get_sitemap_urls, url_insert_bulk
from utils.slack import detailed_error_slack_message

COMPETITOR = "imcdirect"
URL = "https://www.imc-direct.com/sitemap.xml"
MAX_COUNT = 5000


def get_and_store_imcdirect_urls():
    try:
        outputs = []
        sitemap_url = get_sitemap_urls(URL, COMPETITOR)
        for data in sitemap_url:
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
        detailed_error_slack_message(e, COMPETITOR)
