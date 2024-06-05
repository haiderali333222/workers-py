from utils.helpers.index import get_sitemap_urls, url_insert_bulk
from utils.slack import detailed_error_slack_message

COMPETITOR = "mc_mc"
MAIN_SITEMAP_URL = "https://www.mc-mc.com/sitemapindex.xml"
MAX_COUNT = 5000


def get_and_store_mc_mc_urls():
    try:
        outputs = []
        main_sitemap_urls = get_sitemap_urls(MAIN_SITEMAP_URL, COMPETITOR)
        print(f"found {len(main_sitemap_urls)} sitemap urls")

        for url in main_sitemap_urls:
            sitemap_urls = get_sitemap_urls(url, COMPETITOR)

            for sitemap_url in sitemap_urls:
                if "https://www.mc-mc.com/Product/" in sitemap_url:
                    result = {
                        "competitor": COMPETITOR,
                        "url": sitemap_url,
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
