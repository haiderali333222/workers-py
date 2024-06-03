from utils.slack import detailed_error_slack_message
from utils.helpers.index import url_insert_bulk, get_sitemap_urls

COMPETITOR = "chartercontact"
URL = "http://www.chartercontact.com/sitemap.xml"
MAX_COUNT = 5000


def get_and_store_chartercontact_urls():
    try:
        outputs = []
        urls = get_sitemap_urls(URL, COMPETITOR)
        for i in urls:
            result = {
                "competitor": COMPETITOR,
                "url": i,
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
