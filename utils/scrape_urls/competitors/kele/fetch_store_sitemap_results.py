from .helper import store_data
from utils.helpers.index import (
    get_sitemap_urls,
    download_gz_file,
)
from utils.slack import detailed_error_slack_message

COMPETITOR = "kele"
URL = "https://www.kele.com/sitemap-index.xml"


def get_and_store_kele_urls():
    try:
        sitemap_url = get_sitemap_urls(URL, COMPETITOR)
        count = 0
        for data in sitemap_url:
            if ".gz" in data:
                count += 1
                path = download_gz_file(COMPETITOR, data, count)
                store_data(path)
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
