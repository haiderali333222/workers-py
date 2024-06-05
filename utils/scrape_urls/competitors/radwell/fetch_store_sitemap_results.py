from utils.helpers.index import get_sitemap_urls, download_gz_file
from utils.slack import detailed_error_slack_message

from .helper import store_data

COMPETITOR = "radwell"
URL = "https://www.radwell.co.uk/sitemap-index.xml"


def get_and_store_radwell_urls():
    try:
        sitemap_url = get_sitemap_urls(URL, COMPETITOR)
        for count, data in enumerate(sitemap_url, start=1):
            path = download_gz_file(COMPETITOR, data, count)
            store_data(path)
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
