from utils.helpers.index import url_insert_bulk, error_slack_message, get_sitemap_urls

COMPETITOR = "dkhardware"
URL = "https://www.dkhardware.com/sitemap.xml"
MAX_COUNT = 5000


def get_and_store_dkhardware_urls():
    try:
        outputs = []
        urls = get_sitemap_urls(URL, COMPETITOR)
        for data in urls:
            if "/products" in data:
                output_result = get_sitemap_urls(data, COMPETITOR)
                for i in output_result:
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
        error_slack_message(e)
