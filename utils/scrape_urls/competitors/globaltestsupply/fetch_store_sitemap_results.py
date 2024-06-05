from utils.helpers.index import get_sitemap_urls, url_insert_bulk
from utils.slack import detailed_error_slack_message

COMPETITOR = "globaltestsupply"
URL = "https://www.globaltestsupply.com/sitemap.xml"
MAX_COUNT = 5000


def get_and_store_globaltestsupply_urls():
    try:
        outputs = []
        sitemaps_urls = get_sitemap_urls(URL, COMPETITOR)
        for sitemap_url in sitemaps_urls:
            data_sitemap_url = get_sitemap_urls(sitemap_url, COMPETITOR)
            for output in data_sitemap_url:
                result = {
                    "competitor": COMPETITOR,
                    "url": output,
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
