from utils.helpers.index import url_insert_bulk, remove_outdated_urls, get_sitemap_urls
from utils.slack import detailed_error_slack_message

COMPETITOR = "sigmasurplus"
MAX_COUNT = 5000


def get_and_store_sigmasurplus_urls():
    try:
        remove_outdated_urls(COMPETITOR)
        url = "https://sigmasurplus.com/xmlsitemap.php"
        outputs = []
        urls = get_sitemap_urls(url, COMPETITOR)
        for data in urls:
            if "product" in data:
                website_urls = get_sitemap_urls(data, COMPETITOR)
                try:
                    for website_url in website_urls:
                        result = {
                            "competitor": "sigmasurplus",
                            "url": website_url,
                            "scraper_type": "sitemap",
                        }
                        outputs.append(result)
                        if len(outputs) == 5000:
                            url_insert_bulk(outputs)
                            outputs = []
                except Exception as e:
                    detailed_error_slack_message(e, COMPETITOR)
        if outputs and len(outputs):
            url_insert_bulk(outputs)
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
