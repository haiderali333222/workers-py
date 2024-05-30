from utils.helpers.index import url_insert_bulk, error_slack_message, get_sitemap_urls


COMPETITOR = "circuitbreakerwarehouse"
URL = 'https://www.circuitbreakerwarehouse.com/sitemap.xml'
MAX_COUNT = 5000


def get_and_store_circuitbreakerwarehouse_urls():
    try:
        outputs = []
        sitemap_urls = get_sitemap_urls(URL, COMPETITOR)
        for url in sitemap_urls:
            result = {
                "competitor": COMPETITOR,
                "url": url,
                "scraper_type": "sitemap"
            }
            outputs.append(result)
            if len(outputs) == MAX_COUNT:
                url_insert_bulk(outputs)
                outputs = []
        if outputs and len(outputs):
            url_insert_bulk(outputs)
    except Exception as e:
        error_slack_message(e)
