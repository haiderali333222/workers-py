from utils.helpers.index import get_sitemap_urls, url_insert_bulk
from utils.slack import detailed_error_slack_message

COMPETITOR = "unisgroup"
URL = "https://www.unisgroup.com/sitemap.xml"
MAX_COUNT = 5000


def get_and_store_unisgroup_urls():
    try:
        outputs = []
        sitemaps_urls = get_sitemap_urls(URL, COMPETITOR)

        print(f"Found {len(sitemaps_urls)} sitemaps")
        for sitemap_url in sitemaps_urls:
            website_urls = get_sitemap_urls(sitemap_url, COMPETITOR)
            print(f"Found {len(website_urls)} urls in {sitemap_url}")
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
        detailed_error_slack_message(e, COMPETITOR)
