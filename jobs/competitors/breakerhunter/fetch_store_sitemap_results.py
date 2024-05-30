from utils.helpers.index import url_insert_bulk, error_slack_message, get_sitemap_urls


COMPETITOR = "breakerhunter"
URL = "https://breakerhunters.com/sitemap.xml"
MAX_COUNT = 5000


def get_and_store_breakerhunters_urls():
    try:
        sitemap_urls = get_sitemap_urls(URL, COMPETITOR)
        outputs = []
        for sitemap_url in sitemap_urls:
            if "sitemap_products" in sitemap_url:
                website_urls = get_sitemap_urls(sitemap_url, COMPETITOR)
                for website_url in website_urls:
                    if "/products" in website_url:
                        result = {
                            "competitor": COMPETITOR,
                            "url": website_url,
                            "scraper_type": "sitemap",
                        }
                        outputs.append(result)
                        if len(outputs) >= MAX_COUNT:
                            url_insert_bulk(outputs)
                            outputs = []
        if outputs and len(outputs):
            url_insert_bulk(outputs)
    except Exception as e:
        error_slack_message(e)
