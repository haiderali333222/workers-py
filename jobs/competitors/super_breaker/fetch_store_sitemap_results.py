from utils.helpers.index import url_insert_bulk, get_sitemap_urls
from utils.slack import error_slack_message

COMPETITOR = 'superbreakers'
URL = 'https://superbreakers.com/sitemap.xml'
MAX_COUNT = 5000


def get_and_store_superbreakers_urls():
    try:
        sitemaps_urls = get_sitemap_urls(URL, COMPETITOR)
        print(f'Found {len(sitemaps_urls)} sitemaps')
        outputs = []
        for sitemap_url in sitemaps_urls:
            if 'products' in sitemap_url:
                website_urls = get_sitemap_urls(sitemap_url, COMPETITOR)
                print(f'Found {len(website_urls)} urls in {sitemap_url}')
                
                for website_url in website_urls:
                    result = {
                        "competitor": COMPETITOR,
                        "url": website_url,
                        "scraper_type": "sitemap"
                    }
                    outputs.append(result)
                    if len(outputs) == MAX_COUNT:
                        url_insert_bulk(outputs)
                        outputs = []
                        break
        if outputs and len(outputs):
            url_insert_bulk(outputs)
    except Exception as e:
        error_slack_message(e)
