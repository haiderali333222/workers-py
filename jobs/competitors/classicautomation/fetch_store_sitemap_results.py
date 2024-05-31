from utils.helpers.index import url_insert_bulk, get_sitemap_urls
from utils.slack import detailed_error_slack_message

COMPETITOR = "classicautomation"
MAIN_SITEMAP_URL = "https://www.classicautomation.com/sitemap.aspx"


def get_and_store_classic_automation_urls():
    try:
        outputs = []
        sitemaps_urls = get_sitemap_urls(MAIN_SITEMAP_URL, COMPETITOR)

        for sitemap in sitemaps_urls:
            urls = get_sitemap_urls(sitemap, COMPETITOR)
            try:
                for url in urls:
                    if "Part" in url:
                        result = {
                            "competitor": COMPETITOR,
                            "url": url,
                            "scraper_type": "sitemap",
                        }
                        outputs.append(result)
                        if len(outputs) >= 5000:
                            url_insert_bulk(outputs)
                            outputs = []
            except Exception as e:
                detailed_error_slack_message(e, COMPETITOR)
        if outputs and len(outputs):
            url_insert_bulk(outputs)
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
