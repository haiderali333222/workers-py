from utils.helpers.index  import url_insert_bulk, get_sitemap_urls
from utils.slack import error_slack_message

COMPETITOR = 'relectric'
URL = 'https://www.relectric.com/content/sitemap/products-index.xml'
MAX_COUNT = 5000

def get_and_store_relectric_urls():
    try:
        urls = get_sitemap_urls(URL, COMPETITOR)        
        for data in urls:
            output_result = get_sitemap_urls(data, COMPETITOR)
            outputs = []
            for i in output_result:
                result = {
                    "competitor": COMPETITOR,
                    "url": i,
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
